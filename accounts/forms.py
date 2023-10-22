from django import forms
from .models import TextEntry

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