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
from django.shortcuts import render
#from .models import Message
from .forms import SignUpForm
from .models import ResidentUser
from django.contrib.auth import login

from django.urls import reverse
from .models import AdminUser, RaUser, ResidentUser
import datetime
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login

from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from .models import ChatMessage, Task

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Task, ChatMessage, ResidentUser, RaUser

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
    if task.ra != request.user and task.resident != request.user:
        return HttpResponseForbidden("You do not have permission to view this chat.")

    chat_messages = task.chat_messages.all().order_by('timestamp')
    return render(request, 'chat_messages.html', {'chat_messages': chat_messages})

@login_required
def send_message(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if not (ResidentUser.objects.filter(user=request.user, task=task).exists() or
            RaUser.objects.filter(user=request.user, task=task).exists()):
        return HttpResponseForbidden("You are not authorized to send messages in this chat.")

    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            ChatMessage.objects.create(task=task, author=request.user, message=message_text)
            return JsonResponse({'status': 'success', 'message': 'Message sent.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Message cannot be empty.'})
    return HttpResponse(status=405)  # Method Not Allowed

def task_chat(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    # Check permissions here to make sure the user has the right to view and send messages

    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            ChatMessage.objects.create(task=task, author=request.user, message=message_text)
            return JsonResponse({'status': 'success', 'message': 'Message sent.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Message cannot be empty.'})

    chat_messages = task.chat_messages.all().order_by('timestamp')
    return render(request, 'task_chat.html', {'task': task, 'chat_messages': chat_messages})

def open_ticket(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'registration/openTicket.html', {'task': task})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create ResidentUser
            ResidentUser.objects.create(
                user=user, 
                residentName=form.cleaned_data.get('residentName'), 
                floor=form.cleaned_data.get('floor')
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
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})

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
  
   selected_floor = request.GET.get('floor')
   tasks = Task.objects.all()
  
   if selected_floor:
       selected_floor = int(selected_floor)  # Convert to integer
       tasks = tasks.filter(floor=selected_floor)
  
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
    user = RaUser.objects.all()
    tasks = Task.objects.all()
    return render(request, 'registration/profile-view.html', {'user': user, 'tasks':tasks})

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
    tasks = Task.objects.all()
    opened_task_id = None
    if request.method == 'POST':
        opened_task_id = request.POST.get('task_id')

    context = {
        'tasks': tasks,
        'opened_task_id': int(opened_task_id) if opened_task_id else None,
    }
    return render(request, 'registration/residentDashboard.html', context)

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'registration/ticket-success.html')
    else:
        form = TicketForm()
    return render(request, 'registration/ticket-form.html', {'form': form})


