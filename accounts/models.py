from datetime import datetime
from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
class TextEntry(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    floor = models.PositiveIntegerField()
    assingor = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.IntegerField(choices=[(1, 'To Do'), (2, 'In Progress'), (3, 'On Hold'),  (4, 'Done')])
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])
    date_posted = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True)
   
    def __str__(self):
        return self.title
    
class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    room_number = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15, blank=True)

class ManagerUser(CustomUser):
    resident_assistants = models.TextField()

class RaUser(CustomUser):
    floor = models.PositiveIntegerField()
    manager = models.CharField(max_length=200)

class ResidentUser(CustomUser):
    floor = models.PositiveIntegerField()
