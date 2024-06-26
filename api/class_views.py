import ast
import datetime

from django.views import View
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from api.models import User, User_type, Document, DutyList, Document_type
import api.utilities.db_requests as db_requests
from vkr.settings import LOGOUT_REDIRECT_URL


def no_account_no_pass(request):
    if not request.user.is_authenticated:
        return redirect(to=LOGOUT_REDIRECT_URL)


class Home(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(to=LOGOUT_REDIRECT_URL)

        context = {}

        days = {
            "days": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                     28, 29, 30, 31]
        }

        get_room = db_requests.get_rooms_by_user(request)

        context.update(days)
        context.update(get_room)
        context.update(db_requests.get_section_elder(request))

        # TODO fix
        if not request.user.is_staff:

            my_elder_id = User.objects.filter(user_type_id__type="Староста",
                                              room_id__floor=request.user.room_id.floor,
                                              room_id__section=request.user.room_id.section
                                              ).first().id

            get_duty_list_from_db = DutyList.objects.filter(author_id=my_elder_id).first()

            if not get_duty_list_from_db == None:
                duty_list = ast.literal_eval(get_duty_list_from_db.info)
                duty_list = duty_list.pop(request.user.room_id.number)
                context.update({"duty_info": duty_list})

        return render(request, 'views/home.html', context)


class DutyListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(to=LOGOUT_REDIRECT_URL)

        context = {}

        elder_and_assist = db_requests.get_section_elder(request)
        get_room = db_requests.get_rooms_by_user(request)
        # days = {"days": list(range(1, 32))} #  31 дня
        days = {
            "days": list(range(1, 32))
        }

        context.update(elder_and_assist)
        context.update(get_room)
        context.update(days)

        # print(request.user.id)
        # TODO fix
        if not request.user.is_staff:

            my_elder_id = User.objects.filter(user_type_id__type="Староста",
                                              room_id__floor=request.user.room_id.floor,
                                              room_id__section=request.user.room_id.section
                                              ).first().id

            get_duty_list_from_db = DutyList.objects.filter(author_id=my_elder_id).first()

            if not get_duty_list_from_db == None:
                duty_list = get_duty_list_from_db
                context.update({"duty_info": ast.literal_eval(duty_list.info)})

        return render(request, 'views/duty_list.html', context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(to=LOGOUT_REDIRECT_URL)

        # TODO extract from 'post' and 'get' requests: context, days, elder_and_assist, get_room and context updates
        context = {}

        days = {
            "days": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                     28, 29, 30, 31]
        }
        elder_and_assist = db_requests.get_section_elder(request)
        get_room = db_requests.get_rooms_by_user(request)
        context.update(elder_and_assist)
        context.update(get_room)
        context.update(days)

        duty = {}
        for room_i in get_room.get("rooms"):
            duty.update({room_i: []})
        # print(duty)

        server_answer = dict(request.POST)
        server_answer.pop("csrfmiddlewaretoken")  # Delete crsf token
        for day_and_room in server_answer:
            day_and_room = day_and_room.split("-")  # day-room (1-603)
            day = day_and_room[0]
            room = day_and_room[1]

            # if room not in duty.keys():
            #     duty.update({room: []})
            duty[int(room)].append(int(day))

        my_elder_id = User.objects.filter(user_type_id__type="Староста",
                                          room_id__floor=request.user.room_id.floor,
                                          room_id__section=request.user.room_id.section
                                          ).first().id

        get_duty_list_from_db = DutyList.objects.filter(author_id=my_elder_id).first()

        if not get_duty_list_from_db == None:
            get_duty_list_from_db.delete()

        duty_info = DutyList(
            info=str(duty),
            #  TODO plus elder_assist
            author_id=request.user
        )
        duty_info.save()

        context.update({"duty_info": duty})

        return render(request, 'views/duty_list.html', context)


class ResidentsList(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(to=LOGOUT_REDIRECT_URL)

        context = {}

        elder_and_assist = db_requests.get_section_elder(request)
        context.update(elder_and_assist)

        # context.update(util.get_all_users_by_section(request))

        users = db_requests.get_all_users_by_section(request)

        temp_dict_for_users = {}

        #   Code below make form like: {"607": [first_last_name1, first_last_name2], ...}
        for user in users.get("get_all_users_by_section"):
            if not user.get("room_id__number") in temp_dict_for_users:
                temp_dict = {
                    user.get("room_id__number"): [

                        f'{user.get("first_name")} {user.get("last_name")}, {user.get("user_type_id__type")}'

                    ]
                }
                temp_dict_for_users.update(temp_dict)
            else:
                temp_dict_for_users[user.get("room_id__number")].append(
                    f'{user.get("first_name")} {user.get("last_name")}, {user.get("user_type_id__type")}'
                )

        residents = {"residents": temp_dict_for_users}
        context.update(residents)
        context.update(db_requests.get_rooms_by_user(request))

        num_occupied_places_in_rooms = {}
        for room, residents in temp_dict_for_users.items():
            num_occupied_places_in_rooms[room] = len(residents)

        get_rooms_capacity_by_user = db_requests.get_rooms_capacity_by_user(request).get("get_rooms_capacity_by_user")

        empty_place_in_room = []
        for room in get_rooms_capacity_by_user:
            temp = room['capacity']
            room['capacity'] -= num_occupied_places_in_rooms.get(room['number'], 0)
            temp = {'number': room['number'], 'capacity': list(range(room['capacity'])),
                    'no_room': list(range(5 - num_occupied_places_in_rooms.get(room['number'], 0) - room['capacity']))}
            empty_place_in_room.append(temp)

        empty_place_in_room = {"empty_place_in_room": empty_place_in_room}
        context.update(empty_place_in_room)

        return render(request, 'views/residents_list.html', context)


class DocumentsView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(to=LOGOUT_REDIRECT_URL)

        context = {"documents": db_requests.get_all_documents()}

        return render(request, 'views/documents.html', context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(to=LOGOUT_REDIRECT_URL)

        context = {}

        act = dict(request.POST)
        print(act)

        if act.get('delete_file'):
            db_requests.delete_file(request, act['delete_file'])
            pass

        elif request.FILES.get('upload_file'):
            context = db_requests.add_document(request)
            pass

        context.update({"documents": db_requests.get_all_documents()})

        return render(request, 'views/documents.html', context)


