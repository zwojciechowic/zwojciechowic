from django.urls import path
from . import views

app_name = 'hotel'

urlpatterns = [
    path('', views.hotel_home, name='home'),
]