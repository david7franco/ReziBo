from django.core.management.base import BaseCommand
from accounts.models import Task
from accounts.models import RaUser
class Command(BaseCommand):
    help = "Seed the database with test data"

    def handle(self, *args, **options):
    
        #Task.objects.create(title="Task 1", floor=1, assingor='Jane Doe', description="Sample task 1", status=1, priority=1)
        #Task.objects.create(title="Task 2", floor=2, assingor='John Doe', description="Sample task 2", status=2, priority=2)
        #Task.objects.create(title="Task 3", floor=3, assingor='DIO', description="Sample task 3", status=3, priority=3)
        #Task.objects.create(title="Task 4", floor=4, assingor='Jotaro Kujo', description="Sample task 4", status=4, priority=3)
        #Task.objects.create(title="Task 5", floor=5, assingor='Giorno Giovanna', description="This task contains some sample data", status=1, priority=3)
        # Task.objects.all().delete()
        
        # username = "johnsmith"
        # first_name = "John"
        # last_name = "Smith"
        # email = "john.smith@example.com"
        # room_number = 101
        # phone_number = "123-456-7890"
        # floor = 2
        # manager_name = "ManagerName"

        # # Create a RaUser instance
        # RaUser.objects.create(
        #     username=username,
        #     first_name=first_name,
        #     last_name=last_name,
        #     email=email,
        #     room_number=room_number,
        #     phone_number=phone_number,
        #     floor=floor,
        #     manager=manager_name,
        # )



        # Create a RaUser instance
        RaUser.objects.create(
        username='janesmith',
        password='admin@123',
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@example.com',
        room_number=102,
        phone_number='321-654-9870',
        floor=1,
        manager='ManagerName',
        #FK_CustomUser_RaUser=custom_user  # Pass the CustomUser instance here
        )

        

        #Task.objects.create(title="Task 6", description="Sample task 1", status=1)
        self.stdout.write(self.style.SUCCESS("Successfully seeded test data."))