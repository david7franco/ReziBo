from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
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
from .forms import SignUpForm
from .models import ResidentUser
from django.contrib.auth import login

from django.urls import reverse
from .models import AdminUser, RaUser, ResidentUser
import datetime
from django.contrib.auth import authenticate, login as auth_login

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

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


def get_start_end_dates_from_week(year, week):
    firstdayofweek = datetime.datetime.strptime(f'{year}-W{int(week )- 1}-1', "%Y-W%W-%w").date()
    lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)
    return firstdayofweek, lastdayofweek   

def trello_board(request):
    
    selected_floor = request.GET.get('floor')
    tasks = Task.objects.all()
    
    if selected_floor:
        selected_floor = int(selected_floor)  # Convert to integer
        tasks = tasks.filter(floor=selected_floor)
    
    # New time-based filtering logic
    week = request.GET.get('week')
    month = request.GET.get('month')
    year = datetime.datetime.now().year

    if week:
        start_date, end_date = get_start_end_dates_from_week(year, week)
        tasks = tasks.filter(date_posted__gte=start_date, date_posted__lte=end_date)
    elif month:
        tasks = tasks.filter(date_posted__month=month)

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

