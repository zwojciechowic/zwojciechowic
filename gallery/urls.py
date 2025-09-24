from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from . import views
from django.views.generic import TemplateView

path('admin/adjust-photo-position/<int:photo_id>/<str:direction>/', views.admin_adjust_photo_position),