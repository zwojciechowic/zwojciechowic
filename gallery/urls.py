from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('widget/<int:gallery_id>/', views.gallery_widget, name='widget'),
]