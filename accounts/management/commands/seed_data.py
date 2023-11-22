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

        # RAuser 3
        
        user = User.objects.create_user('orpisa38', 'orpisa38@rowan.edu', 'admin@123')

        user.save()
        
        ra_user3 = RaUser(
        user=user,
        floor=2,
        ra_name='Sadia Orpi',
        room_number=101,
        phone_number='123-456-7890',
        ra_email= 'orpisa38@students.rowan.edu'
        )

        ra_user3.save()

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

        #resident user 3
        user= User.objects.create_user('costan42', 'costan42@rowan.edu', 'admin@123')

        user.save()
        
        resdient_user3 = ResidentUser(
        user = user,
        residentName = "Samuel Costantino",
        floor = 1 
        )

        resdient_user3.save()    

        Task.objects.create(title="Help With Cleaning room", floor=1, ra=ra_user, resident=resdient_user, description="I need an RA to come clean my room", status=1, priority=1, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 1, 12, 0)))
        Task.objects.create(title="I need help with cleaning bathroom", floor=1, ra=ra_user,  resident=resdient_user, description="Bathroom needs to be cleaned", status=2, priority=2, date_posted=timezone.make_aware(datetime.datetime(2023, 4, 20, 12, 0)))
        Task.objects.create(title="Bugs in my room ", floor=2, ra=ra_user2, resident=resdient_user2, description="Seems to be a bug infestation in my room", status=3, priority=3, date_posted=timezone.make_aware(datetime.datetime(2023, 9, 15, 12, 0)))
        Task.objects.create(title="Outlet seems to be broken", floor=2, ra=ra_user2, resident=resdient_user2, description="My outlet seems to be broken", status=4, priority=3, date_posted=timezone.make_aware(datetime.datetime(2023, 11, 20, 12, 0)))
        Task.objects.create(title="The heater in my room broke", floor=3, ra=ra_user3, resident=resdient_user3, description="I sleep hot and my heater done broke", status=1, priority=1, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 5, 12, 0)))
        Task.objects.create(title="My AC makes a weird noise", floor=3, ra=ra_user3, resident=resdient_user3, description="I cannot sleep with the annoying sound my AC makes", status=2, priority=2, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 10, 12, 0)))
        Task.objects.create(title="The toilet's cloged", floor=1, ra=ra_user, resident=resdient_user, description="There is a clogged toilet on floor 4", status=3, priority=3, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 15, 12, 0)))
        Task.objects.create(title="The lightbulb in the bathroom died", floor=1, ra=ra_user, resident=resdient_user, description="I can't see what I'm doing in the bathroom", status=4, priority=3, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 20, 12, 0)))
        Task.objects.create(title="The shower only has cold water", floor=2, ra=ra_user2, resident=resdient_user2, description="Can't seem to get hot water from the shower", status=1, priority=1, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 25, 12, 0)))
        Task.objects.create(title="I lost my keys", floor=2, ra=ra_user2, resident=resdient_user2, description="Please let me know if you find them", status=2, priority=2, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 30, 12, 0)))
        Task.objects.create(title="I'm locked out of my room", floor=3, ra=ra_user3, resident=resdient_user3, description="I need to get back in my room please help", status=3, priority=3, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 5, 12, 0)))
        Task.objects.create(title="There's mold in my room", floor=3, ra=ra_user3, resident=resdient_user3, description="This is disgusting, I need to switch rooms", status=4, priority=3, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 10, 12, 0)))
        Task.objects.create(title="I found a pair of keys", floor=1, ra=ra_user, resident=resdient_user, description="Somebody missing their keys?", status=1, priority=1, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 15, 12, 0)))
        Task.objects.create(title="My bike got stolen", floor=1, ra=ra_user, resident=resdient_user, description="I'd like to report a missing bike", status=2, priority=2, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 20, 12, 0)))
        Task.objects.create(title="The bathroom sink is no longer working", floor=2, ra=ra_user2, resident=resdient_user2, description="bathroom sink on floor 8 is out of commision", status=3, priority=3, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 25, 12, 0)))
        Task.objects.create(title="My roomate is missing", floor=2, ra=ra_user2, resident=resdient_user2, description="I haven't seen or heard from the homie, I hope he safe", status=4, priority=3, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 30, 12, 0)))
        Task.objects.create(title="I need an extra key for my room", floor=3, ra=ra_user3, resident=resdient_user3, description="I lost my room key", status=1, priority=1, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 15, 12, 0)))
        Task.objects.create(title="Somebody spilled Pepsi in the lobby", floor=3, ra=ra_user3, resident=resdient_user3, description="Now the floor is all sticky", status=2, priority=2, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 20, 12, 0)))
        Task.objects.create(title="There is furniture missing in the lobby", floor=1, ra=ra_user, resident=resdient_user, description="I could've sworn there was a couch there", status=3, priority=3, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 25, 12, 0)))
        Task.objects.create(title="The lobby TV is broken", floor=1, ra=ra_user, resident=resdient_user, description="Now I can't have movie night with the homies", status=4, priority=3, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 30, 12, 0)))
        Task.objects.create(title="Missing an ID card", floor=2, ra=ra_user2, resident=resdient_user2, description="I can't get inside the building without my ID", status=4, priority=3, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 30, 12, 0)))
        Task.objects.create(title="The neigboors are too loud", floor=2, ra=ra_user2, resident=resdient_user2, description="How am I supposed to study like this?!", status=1, priority=1, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 15, 12, 0)))
        Task.objects.create(title="Eagles watch party, my place", floor=3, ra=ra_user3, resident=resdient_user3, description="Go Birds!!", status=2, priority=2, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 20, 12, 0)))
        Task.objects.create(title="I missplaced my notebook", floor=3, ra=ra_user3, resident=resdient_user3, description="Please let me know if you've found a missing notebook", status=3, priority=3, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 25, 12, 0)))
        Task.objects.create(title="Missing trash can", floor=1, ra=ra_user, resident=resdient_user, description="It is trash day and the trash can in nowhere to be found", status=4, priority=3, date_posted=timezone.make_aware(datetime.datetime(2023, 1, 30, 12, 0)))

        self.stdout.write(self.style.SUCCESS("Successfully seeded test data."))