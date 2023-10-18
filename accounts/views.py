from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from .models import TextEntry
from .forms import TextEntryForm
from django.contrib.auth.decorators import login_required


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