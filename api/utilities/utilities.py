from django.shortcuts import render
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from api.models import User, Room


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

    rooms = sorted(rooms, key=lambda x: x['number'])
    rooms = [d['number'] for d in rooms]

    return {"rooms": rooms}