from django import forms
from django.utils.translation import gettext_lazy as _
from parler.forms import TranslatableModelForm
from .models import Reservation, ContactMessage

class PuppyReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['customer_name', 'customer_email', 'customer_phone']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Wpisz swoje imię i nazwisko'),
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Wpisz swój adres e-mail'),
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Wpisz swój numer telefonu'),
            }),
        }
        labels = {
            'customer_name': _('Imię i nazwisko'),
            'customer_email': _('E-mail'),
            'customer_phone': _('Telefon (opcjonalnie)'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ustaw które pola są wymagane
        self.fields['customer_email'].required = True  # E-mail wymagany
        self.fields['customer_name'].required = False  # Imię opcjonalne
        self.fields['customer_phone'].required = False  # Telefon opcjonalny

class ReservationForm(TranslatableModelForm):
    class Meta:
        model = Reservation
        fields = ['puppy', 'customer_name', 'customer_email', 'customer_phone', 'message']
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
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': _('Dodatkowa wiadomość (opcjonalnie)')
            }),
        }
        labels = {
            'puppy': _('Szczeniak'),
            'customer_name': _('Imię i nazwisko'),
            'customer_email': _('E-mail'),
            'customer_phone': _('Telefon (opcjonalnie)'),
            'message': _('Wiadomość (opcjonalnie)'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ustaw które pola są wymagane
        self.fields['puppy'].required = True  # Szczeniak wymagany
        self.fields['customer_email'].required = True  # E-mail wymagany
        self.fields['customer_name'].required = False  # Imię opcjonalne
        self.fields['customer_phone'].required = False  # Telefon opcjonalny
        self.fields['message'].required = False  # Wiadomość opcjonalna

class ContactForm(TranslatableModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Wpisz swoje imię i nazwisko'),
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Wpisz swój adres email')
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Wpisz swój numer telefonu'),
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Wpisz temat wiadomości'),
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': _('Wpisz swoją wiadomość')
            }),
        }
        labels = {
            'name': _('Imię i nazwisko (opcjonalnie)'),
            'email': _('E-mail'),
            'phone': _('Telefon (opcjonalnie)'),
            'subject': _('Temat (opcjonalnie)'),
            'message': _('Wiadomość'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ustaw które pola są wymagane
        self.fields['email'].required = True  # E-mail wymagany
        self.fields['message'].required = True  # Wiadomość wymagana
        self.fields['name'].required = False  # Imię opcjonalne
        self.fields['phone'].required = False  # Telefon opcjonalny
        self.fields['subject'].required = False  # Temat opcjonalny