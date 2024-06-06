from django.contrib.auth.models import AbstractUser
from django.db import models


class User_type(models.Model):
    type = models.CharField(max_length=50)  # on default set "settler"?

    def __str__(self):
        return self.type


class Building(models.Model):
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.address


class Room(models.Model):
    building_id = models.ForeignKey(Building, on_delete=models.RESTRICT)
    number = models.SmallIntegerField()
    capacity = models.SmallIntegerField()
    floor = models.SmallIntegerField()
    section = models.SmallIntegerField()

    def __str__(self):
        return f"{self.number} {self.floor}.{self.section} | {self.capacity}"


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    user_type_id = models.ForeignKey(User_type, on_delete=models.RESTRICT, null=True)
    room_id = models.ForeignKey(Room, on_delete=models.RESTRICT, null=True)
    study_group = models.CharField(max_length=50, null=True)
    email = models.EmailField()
    is_admin = models.BooleanField(default=False, null=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"phone: {self.phone_number},  email: {self.email}, is_admin: {self.is_admin}"


class Schedule_type(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type


class Schedule(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.RESTRICT, related_name="rooms_seeker")
    schedule_type_id = models.ForeignKey(Schedule_type, on_delete=models.RESTRICT)
    checked_room_id = models.ForeignKey(Room, on_delete=models.RESTRICT, related_name="rooms_checked")
    date = models.DateField(null=True)
    result = models.BooleanField(null=True)

    def __str__(self):
        return f"room_id: {self.room_id}, date: {self.date}, result: {self.result}"


class Document_type(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type


class Document(models.Model):
    document_type_id = models.ForeignKey(Document_type, on_delete=models.RESTRICT)
    author_id = models.ForeignKey(User, on_delete=models.RESTRICT)
    title = models.CharField(max_length=255, null=True)
    file = models.FileField()
    # text = models.TextField(null=True)
    date = models.DateField()

    def __str__(self):
        return f"title: {self.title}, date: {self.date}"


class Feed(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.RESTRICT)
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return f"{self.title}"


class Feed_to_document(models.Model):
    document_id = models.ForeignKey(Document, on_delete=models.RESTRICT)
    feed_id = models.ForeignKey(Feed, on_delete=models.RESTRICT)

    def __str__(self):
        return f"document_id: {self.document_id}, feed_id: {self.feed_id}"


class Document_user(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT)
    document_id = models.ForeignKey(Document, on_delete=models.RESTRICT)
    is_accepted = models.BooleanField()

    def __str__(self):
        return f"document_id: {self.document_id}, user_id: {self.user_id}"


