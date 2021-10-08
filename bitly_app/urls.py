from django.urls import path

from .views import ConvertView, RedirectTo

urlpatterns = [
    path('', ConvertView.as_view(), name='long'),
    path('<str:hash>', RedirectTo.as_view(), name='redirect'),
]