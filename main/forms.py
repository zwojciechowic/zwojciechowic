from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from parler.forms import TranslatableModelForm
from .models import Reservation, ContactMessage

class PuppyReservationForm(forms.ModelForm):
    proposed_price = forms.DecimalField(
        label=_('Twoja propozycja ceny (PLN)'),
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg text-center',
            'placeholder': _('Wpisz swoją propozycję ceny w PLN'),
            'min': '0',
            'step': '100',
        }),
        help_text=_('Podaj swoją propozycję ceny za szczenię')
    )
    
    class Meta:
        model = Reservation
        fields = ['customer_name', 'customer_email', 'customer_phone', 'proposed_price']
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
            'customer_email': _('E-mail*'),
            'customer_phone': _('Telefon*'),
        }
        help_texts = {
            'customer_email': _('* Wymagany email lub telefon'),
            'customer_phone': _('* Wymagany email lub telefon'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Wszystkie pola opcjonalne na poziomie pola
        self.fields['customer_name'].required = False
        self.fields['customer_email'].required = False
        self.fields['customer_phone'].required = False
        self.fields['proposed_price'].required = False

    def clean(self):
        """Niestandardowa walidacja - wymagany email LUB telefon"""
        cleaned_data = super().clean()
        email = cleaned_data.get('customer_email')
        phone = cleaned_data.get('customer_phone')
        proposed_price = cleaned_data.get('proposed_price')

        # Sprawdź czy przynajmniej jedno pole kontaktowe jest wypełnione
        if not email and not phone:
            raise ValidationError(
                _('Musisz podać przynajmniej adres e-mail lub numer telefonu.'),
                code='missing_contact'
            )

        # Opcjonalna walidacja ceny (jeśli chcesz ustawić minimalną wartość)
        if proposed_price is not None and proposed_price < 0:
            raise ValidationError(
                _('Propozycja ceny nie może być ujemna.'),
                code='negative_price'
            )

        return cleaned_data

    def clean_proposed_price(self):
        """Walidacja dla pola proposed_price"""
        proposed_price = self.cleaned_data.get('proposed_price')
        
        if proposed_price is not None:
            if proposed_price < 0:
                raise ValidationError(_('Cena nie może być ujemna.'))
            if proposed_price > 50000:  # Przykładowy limit maksymalny
                raise ValidationError(_('Propozycja ceny wydaje się zbyt wysoka. Sprawdź czy wpisałeś poprawną kwotę.'))
                
        return proposed_price

# forms.py
class ReservationForm(TranslatableModelForm):
    class Meta:
        model = Reservation
        fields = [
            'puppy', 'customer_name', 'customer_email',
            'customer_phone', 'proposed_price', 'message'
        ]
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
            'proposed_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('Zaproponuj swoją cenę (PLN)')
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
            'customer_email': _('E-mail*'),
            'customer_phone': _('Telefon*'),
            'proposed_price': _('Proponowana cena'),
            'message': _('Wiadomość (opcjonalnie)'),
        }
        help_texts = {
            'customer_email': _('* Wymagany email lub telefon'),
            'customer_phone': _('* Wymagany email lub telefon'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Szczeniak wymagany, reszta opcjonalna na poziomie pola
        self.fields['puppy'].required = True
        self.fields['customer_name'].required = False
        self.fields['customer_email'].required = False
        self.fields['customer_phone'].required = False
        self.fields['message'].required = False

    def clean(self):
        """Niestandardowa walidacja - wymagany email LUB telefon"""
        cleaned_data = super().clean()
        email = cleaned_data.get('customer_email')
        phone = cleaned_data.get('customer_phone')

        # Sprawdź czy przynajmniej jedno pole kontaktowe jest wypełnione
        if not email and not phone:
            raise ValidationError(
                _('Musisz podać przynajmniej adres e-mail lub numer telefonu.'),
                code='missing_contact'
            )

        return cleaned_data

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
                'placeholder': _('Wpisz swój adres e-mail')
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
            'email': _('E-mail*'),
            'phone': _('Telefon*'),
            'subject': _('Temat (opcjonalnie)'),
            'message': _('Wiadomość'),
        }
        help_texts = {
            'email': _('* Wymagany email lub telefon'),
            'phone': _('* Wymagany email lub telefon'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Wiadomość wymagana, reszta opcjonalna na poziomie pola
        self.fields['name'].required = False
        self.fields['email'].required = False
        self.fields['phone'].required = False
        self.fields['subject'].required = False
        self.fields['message'].required = True

    def clean(self):
        """Niestandardowa walidacja - wymagany email LUB telefon"""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')

        # Sprawdź czy przynajmniej jedno pole kontaktowe jest wypełnione
        if not email and not phone:
            raise ValidationError(
                _('Musisz podać przynajmniej adres e-mail lub numer telefonu.'),
                code='missing_contact'
            )

        return cleaned_data