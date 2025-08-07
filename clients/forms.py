from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    """Form for creating and updating clients."""
    
    class Meta:
        model = Client
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter client name'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not hasattr(field, 'widget'):
                continue
            if not hasattr(field.widget, 'attrs'):
                field.widget.attrs = {}
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
