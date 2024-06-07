from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from api.models import (
    User,
    User_type,
    Building,
    Room,
    Schedule_type,
    Schedule,
    Document_type,
    Document,
    Feed_to_document,
    Feed,
    Document_user, DutyList
)


#  TODO add "study_group"
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ["first_name", "last_name", "room_id", "user_type_id", "email", "phone_number", "is_admin"]
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            'Доп инфа о пользователя (изменение)',
            {'fields': ("room_id", "user_type_id", "phone_number", "is_admin", )}
        ),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (
            'Доп инфа о пользователя (создание)',
            {'fields': ("first_name", "last_name", "room_id", "user_type_id", "email", "phone_number", "is_admin")}
        ),
    )


class User_typesAdmin(admin.ModelAdmin):
    list_display = ["type"]


class BuildingsAdmin(admin.ModelAdmin):
    list_display = ["address"]


class RoomsAdmin(admin.ModelAdmin):
    list_display = ["number", "building_id"]



admin.site.register(User, UserAdmin)
admin.site.register(User_type, User_typesAdmin)
admin.site.register(Building, BuildingsAdmin)
admin.site.register(Room, RoomsAdmin)
admin.site.register(Schedule_type)
admin.site.register(Schedule)
admin.site.register(Document_type)
admin.site.register(Document)
admin.site.register(DutyList)
admin.site.register(Feed)
admin.site.register(Feed_to_document)
admin.site.register(Document_user)

