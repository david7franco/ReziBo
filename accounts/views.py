from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TextEntry
from .models import RaUser
from .forms import TextEntryForm
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TicketForm
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
#from .models import Message
from .forms import SignUpForm
from .models import ResidentUser
from django.contrib.auth import login
from django.urls import reverse
from .models import AdminUser, RaUser, ResidentUser
import datetime
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse, HttpResponse
from .models import ChatMessage, Task
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Task, ChatMessage, ResidentUser, RaUser
from django.template.loader import render_to_string
from .forms import UserForm
from .forms import UserFormRA
from django.contrib.auth.decorators import login_required

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
'''
def chat_room(request, room_name):
    return render(request, 'chat.html', {'room_name': room_name})

def get_messages(request, room_name):
    messages = Message.objects.filter(room_name=room_name).values('text', 'author', 'timestamp')
    return JsonResponse(list(messages), safe=False)
'''

@login_required
def fetch_messages(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    if hasattr(request.user, 'rauser'): 
        chat_messages = task.chat_messages.all().order_by('timestamp')
    else:
        chat_messages = task.chat_messages.filter(for_ras_only=False).order_by('timestamp')

    return render(request, 'chat_messages.html', {'chat_messages': chat_messages})

'''
def fetch_messages(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    chat_messages = task.chat_messages.all().order_by('timestamp')
    return render(request, 'chat_messages.html', {'chat_messages': chat_messages})
'''

@login_required
def send_message(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    is_ra = hasattr(request.user, 'rauser')
    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        for_ras_only = 'ra_only' in request.POST and is_ra

        if message_text:
            ChatMessage.objects.create(
                task=task,
                author=request.user,
                message=message_text,
                for_ras_only=for_ras_only
            )

            if is_ra:
                chat_messages = task.chat_messages.all().order_by('timestamp')
            else:
                chat_messages = task.chat_messages.filter(for_ras_only=False).order_by('timestamp')

            html = render_to_string('chat_messages.html', {'chat_messages': chat_messages, })
            return HttpResponse(html)
        else:
            return JsonResponse({'status': 'error', 'message': 'Message cannot be empty.'})
    return HttpResponse(status=405)

def task_chat(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        for_ras_only = 'ra_only' in request.POST

        if message_text:
            ChatMessage.objects.create(
                task=task, 
                author=request.user, 
                message=message_text,
                for_ras_only=for_ras_only 
            )
            return JsonResponse({'status': 'success', 'message': 'Message sent.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Message cannot be empty.'})

    chat_messages = task.chat_messages.all().order_by('timestamp')
    is_ra = hasattr(request.user, 'rauser')
    return render(request, 'task_chat.html', {
        'task': task, 
        'chat_messages': chat_messages,
        'is_ra': is_ra 
    })


def open_ticket(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    is_ra = hasattr(request.user, 'rauser')
    return render(request, 'registration/openTicket.html', {'task': task, 'is_ra': is_ra })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create ResidentUser
            ResidentUser.objects.create(
                user=user, 
                residentName=form.cleaned_data.get('residentName'), 
                floor=form.cleaned_data.get('floor'),
                resident_email=form.cleaned_data.get('resident_email'),
                phone_number=form.cleaned_data.get('phone_number'),
                room_number=form.cleaned_data.get('room_number')
            )
            login(request, user)
            # Redirect to home page or wherever you wish
            return redirect('/residentDashboard/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect(redirect_based_on_group(user)) 
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid Username or Password'})

    elif request.user.is_authenticated:
        return redirect(redirect_based_on_group(request.user))
    else:
        return render(request, 'registration/login.html')
    
    
def redirect_based_on_group(user):
    try:
        if hasattr(user, 'adminuser'): 
            return '/admin/'  
        elif (user.is_superuser):
            return '/admin'
        elif hasattr(user, 'rauser'):  
            return '/trello/'  
        elif hasattr(user, 'residentuser'):  
            return '/residentDashboard/'  
        else:
            return reverse('default_dashboard')  
    except (AdminUser.DoesNotExist, RaUser.DoesNotExist, ResidentUser.DoesNotExist):
        return reverse('default_dashboard')  


def get_start_end_dates_from_week(year, month, week):
   print("get start end dates function: Week:", week, "Year:", year)
   # Calculate the first day of the month
   first_day_of_month = datetime.date(year, month, 1)


   # Calculate the start of the week in the context of the month
   days_to_week_start = (week - 1) * 7 - first_day_of_month.weekday()
   week_start_date = first_day_of_month + datetime.timedelta(days=days_to_week_start)


   # The end date is 6 days after the start date
   week_end_date = week_start_date + datetime.timedelta(days=6)


   # Make the datetime objects timezone-aware
   week_start_datetime = timezone.make_aware(datetime.datetime.combine(week_start_date, datetime.time.min))
   week_end_datetime = timezone.make_aware(datetime.datetime.combine(week_end_date, datetime.time.max))
   print("get start end dates function2: week_start:", week_start_datetime, "week_end:", week_end_datetime)
   return week_start_datetime, week_end_datetime

@login_required
def trello_board(request):
  
   selected_floor = request.GET.get('floor', None)
   
   if selected_floor is None:
    try:
        ra_user = RaUser.objects.get(user=request.user)
        if not selected_floor:  # Set default floor only if it's not already set by GET request
            selected_floor = ra_user.floor  # Use RA's floor
    except RaUser.DoesNotExist:
        pass  # The user is not an RA, or RAUser entry does not exist

   #ok tbh idky i need this here but it works so im not questioning the code. -David
   tasks = Task.objects.all()
   
   if selected_floor:
       selected_floor = int(selected_floor)  # Convert to integer
       tasks = tasks.filter(floor=selected_floor)
   else:
       tasks = Task.objects.all()
  
   # New time-based filtering logic
   week = request.GET.get('week')
   month = request.GET.get('month')
   print("Week:", week, "Month:", month)


   year = datetime.datetime.now().year

   if week:
       week = int(week)  # Convert week to integer
       month = int(month)
       start_date, end_date = get_start_end_dates_from_week(year, month, week)
       tasks = tasks.filter(date_posted__gte=start_date, date_posted__lte=end_date)
   elif month:
       tasks = tasks.filter(date_posted__month=month)
   print(tasks.query)  # This will print the raw SQL query

   # Assuming floors range from 1 to 10 (adjust accordingly)
   floors = range(1, 11)
   months = range(1, 13)
   weeks = range(1, 53)
   # Pass all necessary context variables to the template
   context = {
       'tasks': tasks,
       'floors': floors,
       'selected_floor': selected_floor,
       'selected_week': week,
       'selected_month': month,
       'months': months,
       'weeks' : weeks
   }
   return render(request, 'registration/trello.html', context)


@login_required
def profile_view(request):
    user = request.user

    if hasattr(user, 'rauser'):  
        ra_tasks = Task.objects.filter(ra=user.rauser.id)
        return render(request, 'registration/profile-view-rauser.html', {'user': user, 'tasks':ra_tasks})
    else:
        resident_tasks = Task.objects.filter(resident=user.residentuser.id)
        return render(request, 'registration/profile-view.html', {'user': user, 'tasks':resident_tasks})

@csrf_exempt
@require_POST
def move_task(request):
    data = json.loads(request.body)
    task_id = data.get('task_id')
    new_status = data.get('new_status')
    if task_id is not None and new_status is not None:
        task = Task.objects.get(id=task_id)
        task.status = new_status  # Update the status
        task.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def resident_dashboard(request):
    tasks = Task.objects.filter(resident=request.user.residentuser)
    opened_task_id = None
    if request.method == 'POST':
        opened_task_id = request.POST.get('task_id')

    context = {
        'tasks': tasks,
        'opened_task_id': int(opened_task_id) if opened_task_id else None,
    }
    if request.headers.get('HX-Request'):   
        html = render_to_string('registration/task_list.html', context, request)
        return HttpResponse(html)
    return render(request, 'registration/residentDashboard.html', context)

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            # Create an instance of the ticket but don't save it yet
            new_ticket = form.save(commit=False)
            print(RaUser.objects.filter(floor=request.user.residentuser.floor))
            rau = RaUser.objects.filter(floor=request.user.residentuser.floor)[0]
            new_ticket.ra = rau
            # Set the floor attribute from the resident's floor
            new_ticket.floor = request.user.residentuser.floor
            new_ticket.resident = request.user.residentuser
            # Now save the ticket to the database
            new_ticket.save()

            return render(request, 'registration/ticket-success.html')
    else:
        form = TicketForm()

    return render(request, 'registration/ticket-form.html', {'form': form})

def edit_ticket(request, task_id):
    # retrieve the given instance of the task
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return render(request, 'registration/ticket-success.html')
    else:
        form = TicketForm(instance=task)
    return render(request, 'registration/ticket-form.html', {'form': form, 'task': task})


def edit_profile(request):
    resident_user = request.user.residentuser

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=resident_user)
        if form.is_valid():
            form.save()
            return redirect('profile-view')
    else:
        form = UserForm(instance=resident_user)

    return render(request, 'registration/edit-profile.html', {'form': form, 'resident_user': resident_user})

def edit_profile_ra(request):
    ra_user = request.user

    if request.method == 'POST':
        form = UserFormRA(request.POST, request.FILES, instance=ra_user.rauser)
        if form.is_valid():
            form.save()
    else:
        form = UserForm(instance=ra_user)

    return render(request, 'registration/edit-profile-ra.html', {'form': form, 'rauser': ra_user})
