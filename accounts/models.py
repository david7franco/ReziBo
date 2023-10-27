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
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    floor = models.PositiveIntegerField(default=0)
    # assingor = models.ForeignKey(User, on_delete=models.CASCADE)
    assingor = models.CharField(max_length=200, default='Null')
    description = models.TextField()
    status = models.IntegerField(choices=[(1, 'To Do'), (2, 'In Progress'), (3, 'On Hold'),  (4, 'Done')])
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=1)
    date_posted = models.DateTimeField(default=datetime.now)
    # image = models.ImageField(blank=True)
   
    def __str__(self):
        return self.title
    
class CustomUser(AbstractUser):
    room_number = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15, blank=True)

    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='customuser_set')
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='customuser_set'
    )

class ManagerUser(CustomUser):
    is_admin = models.BooleanField(default=True)
    is_r_a = models.BooleanField(default=False)
    is_resident = models.BooleanField(default=False)
    resident_assistants = models.TextField()

class RaUser(CustomUser):
    is_admin = models.BooleanField(default=False)
    is_r_a = models.BooleanField(default=True)
    is_resident = models.BooleanField(default=False)
    floor = models.PositiveIntegerField()
    manager = models.CharField(max_length=200)

class ResidentUser(CustomUser):
    is_admin = models.BooleanField(default=False)
    is_r_a = models.BooleanField(default=False)
    is_resident = models.BooleanField(default=True)
    floor = models.PositiveIntegerField()