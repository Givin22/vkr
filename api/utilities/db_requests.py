from datetime import datetime

from django.shortcuts import render
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from api.models import User, Room, Document, Document_type


# TODO Check that two objects won't return (two elder or two assist)
# Return first_name, last_name and room number of "elder" and "assistant_elder"
def get_section_elder(request) -> dict:
    current_user = request.user
    current_user_floor = current_user.room_id.floor
    current_user_section = current_user.room_id.section

    elder = "Отсутствует"
    assistant_elder = "Отсутствует"

    try:
        elder_of_current_user = User.objects.filter(
            Q(user_type_id__type="Староста") &
            Q(room_id__floor=current_user_floor) &
            Q(room_id__section=current_user_section)
        ).get()
        elder = f"{elder_of_current_user.first_name}\
                  {elder_of_current_user.last_name}\
                  {elder_of_current_user.room_id.number}"
    except ObjectDoesNotExist:
        pass

    try:
        assist_elder_of_current_user = User.objects.filter(
            Q(user_type_id__type="ЗамСтаросты") &
            Q(room_id__floor=current_user_floor) &
            Q(room_id__section=current_user_section)
        ).get()
        assistant_elder = f"{assist_elder_of_current_user.first_name}\
                            {assist_elder_of_current_user.last_name}\
                            {assist_elder_of_current_user.room_id.number}"
    except ObjectDoesNotExist:
        pass

    return {"elder": elder, "assistant_elder": assistant_elder}


def get_rooms_by_user(request):
    current_user = request.user
    current_user_floor = current_user.room_id.floor
    current_user_section = current_user.room_id.section

    rooms = list(Room.objects.filter(
        Q(floor=current_user_floor) &
        Q(section=current_user_section)
    ).all().values("number"))

    rooms = sorted(rooms, key=lambda field: field['number'])
    rooms = [room['number'] for room in rooms]

    return {"rooms": rooms}


def get_all_users_by_section(request):
    current_user = request.user
    current_user_floor = current_user.room_id.floor
    current_user_section = current_user.room_id.section

    users = list(User.objects.filter(
        Q(room_id__floor=current_user_floor) &
        Q(room_id__section=current_user_section)
    ).all().values("first_name", "last_name", "room_id__number", "user_type_id__type"))

    users.sort(key=lambda x: x['room_id__number'])

    return {"get_all_users_by_section": users}


def get_rooms_capacity_by_user(request):
    current_user = request.user
    current_user_floor = current_user.room_id.floor
    current_user_section = current_user.room_id.section

    rooms_capacity = list(Room.objects.filter(
        Q(floor=current_user_floor) &
        Q(section=current_user_section)
    ).all().values("number", "capacity"))

    rooms_capacity.sort(key=lambda x: x['number'])

    rooms_capacity = [
        {'number': room.get("number"), 'capacity': room['capacity']}
        for room in rooms_capacity
    ]

    return {"get_rooms_capacity_by_user": rooms_capacity}


#  TODO make it
def get_all_documents():
    # print(Document.objects.first())
    # print(Document.objects.all())
    # print(list(Document.objects.all()))
    # return Document.objects.first()

    return list(Document.objects.all())


def add_document(request):
    file = request.FILES['upload_file']

    if Document.objects.filter(title=file.name).first():
        return {"result": "Файл уже существует! Удалите старый и повторите"}

    save_file_DB = Document(
        document_type_id=Document_type.objects.filter(type="Администрация").first(),
        author_id=User.objects.filter(username=request.user.username).first(),
        title=file.name,
        file=file,
        date=datetime.today()
    )
    save_file_DB.save()

    return {"result": "Файл сохранён!"}
