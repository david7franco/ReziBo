from datetime import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import User
'''
User = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username + ": " + self.text[:50]

    class Meta:
        ordering = ('timestamp',)
'''

# Create your models here.
class TextEntry(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class AdminUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_name = models.TextField()
    image = models.ImageField(null=True, blank=True)



class RaUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    floor = models.PositiveIntegerField()
    ra_name = models.CharField(max_length=200)
    room_number = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15, blank=True)
    ra_email = models.EmailField(default=None)
    image = models.ImageField(null=True, upload_to='media/accounts/static')



class ResidentUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    residentName = models.CharField(max_length=200)
    floor = models.PositiveIntegerField()
    resident_email = models.EmailField(default=None, max_length=254)
    phone_number = models.CharField(max_length=15, blank=True)
    room_number = models.PositiveIntegerField(default = 0)
    image = models.ImageField(null=True, blank=True, upload_to='media/accounts/static')



class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    floor = models.PositiveIntegerField(default=0)
    description = models.TextField()
    ra = models.ForeignKey(RaUser, related_name='ra_tasks', on_delete=models.SET_NULL, null=True, blank=True)
    resident = models.ForeignKey(ResidentUser, related_name='resident_tasks', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField(
        choices=[(1, "To Do"), (2, "In Progress"), (3, "On Hold"), (4, "Done")],
        default=1,
    )
    priority = models.IntegerField(
        choices=[(1, "Low"), (2, "Medium"), (3, "High")], default=1
    )
    date_posted = models.DateTimeField(default=timezone.now)
    task_deadline = models.DateField(null= True, blank=True, default=timezone.now)
    image = models.ImageField(null=True, blank=True, upload_to='media/accounts/static')
    file = models.FileField(null=True, blank=True, upload_to='media/accounts/static')

    def __str__(self):
        return self.title
    
class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    fk_task_comment = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_posted = models.DateTimeField(default=datetime.now)



class Annotations(models.Model):
    annotate_id = models.AutoField(primary_key=True)
    fk_task_annotations = models.ForeignKey(Task, related_name='annotations', on_delete=models.CASCADE)
    annotations = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_posted = models.DateTimeField(default=datetime.now)


class ChatMessage(models.Model):
    task = models.ForeignKey(Task, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    for_ras_only = models.BooleanField(default=False)

    def __str__(self):
        return f"Message by {self.author.username} for Task {self.task.id}"