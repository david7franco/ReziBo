from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TextEntry
from .forms import TextEntryForm
from django.contrib.auth.decorators import login_required
from .models import Task
from django.views.decorators.http import require_POST
import json

from django.contrib.auth import authenticate, login as auth_login

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

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
    '''
    if (user.get_group() is "RA"):
        return '/trello/'
    elif (user.get_group() is "Resident"):
        return '/residentDashboard/'
    else:
        return '/admin/'
    '''
    if not(user.is_superuser):
        return '/residentDashboard/' 
    return '/admin/'  

@login_required
def text_entry(request):
    if request.method == 'POST':
        form = TextEntryForm(request.POST, user=request.user)  # Pass the user to the form
        if form.is_valid():
            form.save()
            return redirect('text_display')
    else:
        form = TextEntryForm(user=request.user)  # Pass the user to the form

    return render(request, 'registration/text-entry.html', {'form': form})

def text_display(request):
    entries = TextEntry.objects.all()
    return render(request, 'registration/text-display.html', {'entries': entries})

def trello_board(request):
    
    selected_floor = request.GET.get('floor')
    if selected_floor:
        selected_floor = int(selected_floor)  # Convert to integer
        tasks = Task.objects.filter(floor=selected_floor)
    else:
        tasks = Task.objects.all()


    # Assuming floors range from 1 to 10 (adjust accordingly)
    floors = range(1, 11)

    return render(request, 'registration/trello.html', {'tasks': tasks, 'floors': floors, 'selected_floor': selected_floor})

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