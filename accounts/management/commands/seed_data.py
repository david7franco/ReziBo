import datetime
from django.core.management.base import BaseCommand
from accounts.models import Task
from accounts.models import RaUser
from accounts.models import User
from accounts.models import ResidentUser
import datetime
from django.utils import timezone
class Command(BaseCommand):
    help = "Seed the database with test data"

    def handle(self, *args, **options):
    
        Task.objects.create(title="Help With Cleaning room", floor=1, assingor='Jane Doe', description="I need an RA to come clean my room", status=1, priority=1, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 1, 12, 0)))
        Task.objects.create(title="I need help with cleaning bathroom", floor=2, assingor='John Doe', description="Bathroom needs to be cleaned", status=2, priority=2, date_posted=timezone.make_aware(datetime.datetime(2023, 4, 20, 12, 0)))
        Task.objects.create(title="Bugs in my room ", floor=3, assingor='DIO', description="Seems to be a bug infestation in my room", status=3, priority=3, date_posted=timezone.make_aware(datetime.datetime(2023, 9, 15, 12, 0)))
        Task.objects.create(title="Outlet seems to be broken", floor=4, assingor='Jotaro Kujo', description="My outlet seems to be broken", status=4, priority=3, date_posted=timezone.make_aware(datetime.datetime(2023, 11, 20, 12, 0)))
        #Task.objects.all().delete()


        user= User.objects.create_user('franco13', 'franco13@rowan.edu', 'Totonaca13!')

        user.save()
        
        ra_user = RaUser(
        user=user,
        floor=1,
        ra_name='David Franco',
        room_number=101,
        phone_number='123-456-7890',
        ra_email= 'franco13@students.rowan.edu'
        )

        ra_user.save()
        
        user= User.objects.create_user('patels13', 'patels13@rowan.edu', 'admin@123')

        user.save()
        
        resdient_user = ResidentUser(
        user = user,
        residentName = "Shivang Patel",
        floor = 1 
        )

        resdient_user.save()


        #Task.objects.create(title="Task 6", description="Sample task 1", status=1)
        self.stdout.write(self.style.SUCCESS("Successfully seeded test data."))