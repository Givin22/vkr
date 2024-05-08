from django.contrib import admin
from api.models import Users


class UserAdmin(admin.ModelAdmin):
    list_display = ["email"]


admin.site.register(Users, UserAdmin)
