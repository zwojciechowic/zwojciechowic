from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Reservation, ContactMessage

class PuppyReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['customer_name', 'customer_email', 'customer_phone']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Wpisz swoje imię i nazwisko'),
                'required': True
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Wpisz swój adres e-mail'),
                'required': True
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Wpisz swój numer telefonu'),
                'required': True
            }),
        }
        labels = {
            'customer_name': _('Imię i nazwisko'),
            'customer_email': _('E-mail'),
            'customer_phone': _('Telefon'),
        }

# Tymczasowo BEZ 'message' w fields - dodaj po makemigrations
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['puppy', 'customer_name', 'customer_email', 'customer_phone']  # <- usunieto 'message'
        widgets = {
            'puppy': forms.Select(attrs={'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Tymczasowo BEZ 'subject', 'message' w fields - dodaj po makemigrations  
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone']  # <- usunieto 'subject', 'message'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }