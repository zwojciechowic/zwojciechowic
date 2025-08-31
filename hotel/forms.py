from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ['created_at']
        widgets = {
            'owner_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jan Kowalski'}),
            'owner_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'jan@example.com'}),
            'owner_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+48 123 456 789'}),
            'dog_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Burek'}),
            'dog_breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Labrador'}),
            'dog_age': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'date_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_to': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'additional_services': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Opcjonalne usługi dodatkowe'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to and date_from >= date_to:
            raise forms.ValidationError('Data zakończenia musi być późniejsza niż data rozpoczęcia.')
        
        return cleaned_data