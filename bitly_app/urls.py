from django.urls import path

from .views import ConvertView, RedirectTo

urlpatterns = [
    path('long', ConvertView.as_view(), name='long'),
    path('<str:hash_url>', RedirectTo.as_view(), name='redirect'),
]