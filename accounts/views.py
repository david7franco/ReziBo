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


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


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
    tasks = Task.objects.all()
    return render(request, 'registration/trello.html', {'tasks': tasks})

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
    return render(request, 'registration/residentDashboard.html')