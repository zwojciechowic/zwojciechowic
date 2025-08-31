from django.db import models
from django.core.validators import EmailValidator, RegexValidator

class Booking(models.Model):
    owner_name = models.CharField("Imię i nazwisko", max_length=100)
    owner_email = models.EmailField("E-mail", validators=[EmailValidator()])
    owner_phone = models.CharField("Telefon", max_length=15, validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    
    dog_name = models.CharField("Imię psa", max_length=50)
    dog_breed = models.CharField("Rasa", max_length=50)
    dog_age = models.PositiveIntegerField("Wiek psa")
    
    date_from = models.DateField("Data rozpoczęcia")
    date_to = models.DateField("Data zakończenia")
    
    additional_services = models.TextField("Usługi dodatkowe", blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.owner_name} - {self.dog_name}"
    
    class Meta:
        verbose_name = "Rezerwacja"
        verbose_name_plural = "Rezerwacje"

class FAQ(models.Model):
    question = models.CharField("Pytanie", max_length=200)
    answer = models.TextField("Odpowiedź")
    order = models.PositiveIntegerField("Kolejność", default=1)
    
    def __str__(self):
        return self.question
    
    class Meta:
        ordering = ['order']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"