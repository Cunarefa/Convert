from django.urls import path

from .views import ConvertView

urlpatterns = [
    path('long', ConvertView.as_view(), name='long'),
]