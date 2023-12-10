from django import forms
from .models import TextEntry
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from .models import RaUser
from .models import ResidentUser
from .models import User
from django.core.validators import RegexValidator
from django.contrib.admin.widgets import AdminDateWidget

class UserForm(forms.ModelForm):
    class Meta:
        model = ResidentUser
        fields = ['image', 'residentName', 'resident_email', 'phone_number']

class UserFormRA(forms.ModelForm):
    class Meta:
        model = RaUser
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

'''
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']
'''

class DateInput(forms.DateInput):
    input_type = 'date'


class TicketForm(forms.ModelForm):     
    task_deadline = forms.DateField(label='Date Deadline', required=False, widget=DateInput)
    class Meta:
        model = Task
        fields = ['title', 'priority', 'description', 'task_deadline', 'image', 'file']
        

class SignUpForm(UserCreationForm):
    residentName = forms.CharField(
        max_length=200, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'}) # Add Bootstrap class here
    )
    resident_email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    floor = forms.IntegerField(
        min_value=1, 
        max_value=4, 
        required=True, 
        widget=forms.NumberInput(attrs={'class': 'form-control'}) # Add Bootstrap class here
    )
    room_number = forms.IntegerField(
        min_value=100, 
        max_value=400, 
        required=True, 
        widget=forms.NumberInput(attrs={'class': 'form-control'}) # Add Bootstrap class here
    )
    phone_number = forms.CharField(
        max_length=15, 
        required=False,  # Set to True if the field is mandatory
        validators=[
            RegexValidator(
                r'^\d{3}-\d{3}-\d{4}$', 
                message="Phone number must be entered in the format: '999-999-9999'."
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'In this format: 999-999-9999'})
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('residentName', 'resident_email', 'phone_number', 'floor', 'room_number')





'''
class SignUpForm(UserCreationForm):
    residentName = forms.CharField(max_length=200, required=True)
    floor = forms.IntegerField(min_value=1, max_value=10, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('residentName', 'floor')
'''