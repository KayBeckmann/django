from django.urls import path
from . import views

urlpatterns = [
  path('', views.start, name='start'),
  path('hallo/', views.hallo,name='hallo')
]