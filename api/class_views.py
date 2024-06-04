from django.views import View
from django.shortcuts import render
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from api.models import User, User_type
import api.utilities.utilities as util


class Home(View):
    def get(self, request):
        context = util.get_section_elder(request)

        return render(request, 'views/home.html', context)


class DutyList(View):
    def get(self, request):
        context = {}

        elder_and_assist = util.get_section_elder(request)
        get_room = util.get_rooms_by_user(request)
        days = {
            "days": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                     28, 29, 30, 31]
        }

        context.update(elder_and_assist)
        context.update(get_room)
        context.update(days)

        return render(request, 'views/duty_list.html', context)

    def post(self, request):
        mass = []
        for i in request.POST.items():
            mass.append(i)
        # for key, value in request.POST.items():
        #     test = {key: value}
        #     mass.append(test)
        context = {"info": mass}

        return render(request, 'views/duty_list.html', context)


class ResidentsList(View):
    def get(self, request):
        context = {}

        elder_and_assist = util.get_section_elder(request)
        context.update(elder_and_assist)

        # context.update(util.get_all_users_by_section(request))

        users = util.get_all_users_by_section(request)

        temp_dict_for_users = {}

        #   Code below make form like: {"607": [[first_name], [last_name]], "608": [[first_name], [last_name]] ...}
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
        context.update(util.get_rooms_by_user(request))

        num_occupied_places_in_rooms = {}
        for room, residents in temp_dict_for_users.items():
            num_occupied_places_in_rooms[room] = len(residents)

        get_rooms_capacity_by_user = util.get_rooms_capacity_by_user(request).get("get_rooms_capacity_by_user")

        empty_place_in_room = []
        for room in get_rooms_capacity_by_user:
            temp = room['capacity']
            room['capacity'] -= num_occupied_places_in_rooms.get(room['number'], 0)
            temp = {'number': room['number'], 'capacity': list(range(room['capacity'])), 'no_room': list(range(5 - num_occupied_places_in_rooms.get(room['number'], 0) - room['capacity']))}
            empty_place_in_room.append(temp)

        empty_place_in_room = {"empty_place_in_room": empty_place_in_room}
        context.update(empty_place_in_room)

        return render(request, 'views/residents_list.html', context)
