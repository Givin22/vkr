from django.db import models


class Profiles(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50)
    phone_number = models.Field


class User_types(models.Model):
    type = models.CharField(max_length=50) # on default set "settler"?


class Buildings(models.Model):
    address = models.CharField(max_length=255)


class Rooms(models.Model):
    building_id = models.ForeignKey(Buildings, on_delete=models.RESTRICT)
    number = models.SmallIntegerField()
    capacity = models.SmallIntegerField()
    floor = models.SmallIntegerField()
    section = models.SmallIntegerField()


class Users(models.Model):
    profile_id = models.ForeignKey(Profiles, on_delete=models.RESTRICT)
    user_type_id = models.ForeignKey(User_types, on_delete=models.RESTRICT)
    room_id = models.ForeignKey(Rooms, on_delete=models.RESTRICT)
    email = models.EmailField()
    is_admin = models.BooleanField(default=False)


class Schedule_types(models.Model):
    type = models.CharField(max_length=255)


class Schedule(models.Model):
    room_id = models.ForeignKey(Rooms, on_delete=models.RESTRICT, related_name="rooms_seeker")
    schedule_type_id = models.ForeignKey(Schedule_types, on_delete=models.RESTRICT)
    checked_room_id = models.ForeignKey(Rooms, on_delete=models.RESTRICT, related_name="rooms_checked")
    date = models.DateField
    result = models.BooleanField(null=True)


class Document_types(models.Model):
    type = models.CharField(max_length=255)


class Documents(models.Model):
    document_type_id = models.ForeignKey(Document_types, on_delete=models.RESTRICT)
    author_id = models.ForeignKey(Users, on_delete=models.RESTRICT)
    title = models.CharField(max_length=255, null=True)
    file = models.BinaryField()
    date = models.DateField()


class Feeds(models.Model):
    author_id = models.ForeignKey(Users, on_delete=models.RESTRICT)
    title = models.CharField(max_length=255)
    text = models.TextField()


class Feed_to_document(models.Model):
    document_id = models.ForeignKey(Documents, on_delete=models.RESTRICT)
    feed_id = models.ForeignKey(Feeds, on_delete=models.RESTRICT)


class Document_users(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.RESTRICT)
    document_id = models.ForeignKey(Documents, on_delete=models.RESTRICT)
    is_accepted = models.BooleanField()


