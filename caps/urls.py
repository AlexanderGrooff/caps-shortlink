from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_long_url, name='index'),
    path('L/<str:checksum>/', views.redirect_checksum),
]
