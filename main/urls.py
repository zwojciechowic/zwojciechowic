from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path(_('o-nas/'), views.about, name='about'),
    path(_('nasze-psy/'), views.dogs, name='dogs'),
    path(_('szczeniaki/'), views.puppies, name='puppies'),
    path(_('rezerwacje/'), views.reservations, name='reservations'),
    path(_('kontakt/'), views.contact_view, name='contact'),
]