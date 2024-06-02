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
                     28, 29, 30, 31]}

        context.update(elder_and_assist)
        context.update(get_room)
        context.update(days)

        return render(request, 'views/duty_list.html', context)

    def post(self, request):
        context = {}
        mass = []
        for i in request.POST.items():
            mass.append(i)
        # for key, value in request.POST.items():
        #     test = {key: value}
        #     mass.append(test)
        context = {"info": mass}

        return render(request, 'views/duty_list.html', context)
