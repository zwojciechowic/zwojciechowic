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

class ReservationForm(forms.ModelForm):
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 4,
            'placeholder': _('Dodatkowa wiadomość (opcjonalnie)')
        }),
        label=_('Wiadomość')
    )
    
    class Meta:
        model = Reservation
        fields = ['puppy', 'customer_name', 'customer_email', 'customer_phone']
        widgets = {
            'puppy': forms.Select(attrs={'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Wpisz swoje imię i nazwisko')
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Wpisz swój adres e-mail')
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Wpisz swój numer telefonu')
            }),
        }
        labels = {
            'puppy': _('Szczeniak'),
            'customer_name': _('Imię i nazwisko'),
            'customer_email': _('E-mail'),
            'customer_phone': _('Telefon'),
        }

class ContactForm(forms.ModelForm):
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Wpisz temat wiadomości')
        }),
        label=_('Temat')
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': _('Wpisz swoją wiadomość')
        }),
        label=_('Wiadomość')
    )
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Wpisz swoje imię i nazwisko')
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Wpisz swój adres email')
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Wpisz swój numer telefonu')
            }),
        }
        labels = {
            'name': _('Imię i nazwisko'),
            'email': _('E-mail'),
            'phone': _('Telefon'),
        }