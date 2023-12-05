from django import forms
from .models import TextEntry
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from .models import RaUser
from .models import ResidentUser
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = ResidentUser
        fields = ['image']

class TextEntryForm(forms.ModelForm):
    class Meta:
        model = TextEntry
        fields = ['content', 'user']  

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super(TextEntryForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user
            self.fields['user'].widget = forms.HiddenInput()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'priority', 'description', 'image', 'file']


class SignUpForm(UserCreationForm):
    residentName = forms.CharField(
        max_length=200, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'}) # Add Bootstrap class here
    )
    floor = forms.IntegerField(
        min_value=1, 
        max_value=10, 
        required=True, 
        widget=forms.NumberInput(attrs={'class': 'form-control'}) # Add Bootstrap class here
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('residentName', 'floor')





'''
class SignUpForm(UserCreationForm):
    residentName = forms.CharField(max_length=200, required=True)
    floor = forms.IntegerField(min_value=1, max_value=10, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('residentName', 'floor')
'''