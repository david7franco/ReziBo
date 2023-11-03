from datetime import datetime
from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.utils.translation import gettext as _


# Create your models here.
class TextEntry(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Task(models.Model):
    TaskId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    floor = models.PositiveIntegerField(default=0)
    # assingor = models.ForeignKey(User, on_delete=models.CASCADE)
    assingor = models.CharField(max_length=200, default="Null")
    description = models.TextField()
    status = models.IntegerField(
        choices=[(1, "To Do"), (2, "In Progress"), (3, "On Hold"), (4, "Done")],
        default=1,
    )
    priority = models.IntegerField(
        choices=[(1, "Low"), (2, "Medium"), (3, "High")], default=1
    )
    date_posted = models.DateTimeField(default=datetime.now)
    # image = models.ImageField(blank=True)

    def __str__(self):
        return self.title


#class CustomUser(models.Model):
    # #customUserID = models.AutoField(primary_key=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # room_number = models.PositiveIntegerField()
    # phone_number = models.CharField(max_length=15, blank=True)
    # username = models.CharField(max_length=20, blank=True )
    # first_name = models.CharField(max_length=50, blank=True )
    # last_name = models.CharField(max_length=50, blank=True )
    # email = models.EmailField(max_length=200, blank=True )

    # groups = models.ManyToManyField(
    #     Group, verbose_name=_("groups"), blank=True, related_name="customuser_set"
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     verbose_name=_("user permissions"),
    #     blank=True,
    #     related_name="customuser_set",
    # )


class AdminUser(models.Model):
    #managerID = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resident_assistants = models.TextField()


class RaUser(models.Model):
    #RaID = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    floor = models.PositiveIntegerField()
    manager = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room_number = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15, blank=True)
    username = models.CharField(max_length=20, blank=True )
    first_name = models.CharField(max_length=50, blank=True )
    last_name = models.CharField(max_length=50, blank=True )
    email = models.EmailField(max_length=200, blank=True )
    password = models.CharField(max_length=50)


class ResidentUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #resdidentID = models.AutoField(primary_key=True)
    residentName = models.CharField(max_length=200)
    floor = models.PositiveIntegerField()
