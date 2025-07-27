from django import forms
from .models import Reservation, ContactMessage

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['puppy', 'customer_name', 'customer_email', 'customer_phone', 'message']
        widgets = {
            'puppy': forms.Select(attrs={'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class PuppyReservationForm(forms.ModelForm):
    """Formularz rezerwacji dla konkretnego szczenięcia (bez wyboru szczenięcia)"""
    class Meta:
        model = Reservation
        fields = ['customer_name', 'customer_email', 'customer_phone', 'message']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Wpisz swoje imię i nazwisko'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Wpisz swój email'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Wpisz swój numer telefonu'
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Wpisz temat wiadomości'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Wpisz swoją wiadomość'
        })
    )