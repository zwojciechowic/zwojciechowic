# main/urls.py
from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path(_('o-nas/'), views.about, name='about'),
    path(_('nasze-psy/'), views.dogs, name='dogs'),
    path(_('nasze-psy/<int:pk>/'), views.dog_detail, name='dog_detail'),
    path(_('szczeniaki/'), views.puppies, name='puppies'),
    path(_('szczeniaki/<int:pk>/'), views.puppy_detail, name='puppy_detail'),
    path(_('rezerwacje/'), views.reservations, name='reservations'),
    path(_('kontakt/'), views.contact_view, name='contact'),
    path(_('hotel/'), views.hotel, name='hotel'),
]