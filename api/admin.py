from django.contrib import admin
from api.models import Author


class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name"]


admin.site.register(Author, UserAdmin)
