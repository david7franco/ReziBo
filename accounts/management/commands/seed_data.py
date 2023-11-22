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
    
            
        #Task.objects.all().delete()

        # RAuser 1
        user= User.objects.create_user('franco13', 'franco13@rowan.edu', 'admin@123')

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
        ###########################################################################

        # RAuser 2
        
        user = User.objects.create_user('elliot93', 'elliot93@rowan.edu', 'admin@123')

        user.save()
        
        ra_user2 = RaUser(
        user=user,
        floor=2,
        ra_name='Ethan Elliott',
        room_number=101,
        phone_number='123-456-7890',
        ra_email= 'elliot93@students.rowan.edu'
        )

        ra_user2.save()

        ###########################################################################


        # Resident user 1
        user= User.objects.create_user('patels13', 'patels13@rowan.edu', 'admin@123')

        user.save()
        
        resdient_user = ResidentUser(
        user = user,
        residentName = "Shivang Patel",
        floor = 1 
        )

        resdient_user.save()

        # Resident user 2
        user= User.objects.create_user('patels47', 'patels47@rowan.edu', 'admin@123')

        user.save()
        
        resdient_user2 = ResidentUser(
        user = user,
        residentName = "Shivam Patel",
        floor = 1 
        )

        resdient_user2.save()

        Task.objects.create(title="Help With Cleaning room", floor=1, ra=ra_user, resident=resdient_user, description="I need an RA to come clean my room", status=1, priority=1, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 1, 12, 0)))
        Task.objects.create(title="I need help with cleaning bathroom", floor=1, ra=ra_user,  resident=resdient_user, description="Bathroom needs to be cleaned", status=2, priority=2, date_posted=timezone.make_aware(datetime.datetime(2023, 4, 20, 12, 0)))
        Task.objects.create(title="Bugs in my room ", floor=2, ra=ra_user2, resident=resdient_user2, description="Seems to be a bug infestation in my room", status=3, priority=3, date_posted=timezone.make_aware(datetime.datetime(2023, 9, 15, 12, 0)))
        Task.objects.create(title="Outlet seems to be broken", floor=2, ra=ra_user2, resident=resdient_user2, description="My outlet seems to be broken", status=4, priority=3, date_posted=timezone.make_aware(datetime.datetime(2023, 11, 20, 12, 0)))

        self.stdout.write(self.style.SUCCESS("Successfully seeded test data."))