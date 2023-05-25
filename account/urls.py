from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('hello/', views.hello_world, name='hello_world'),
    path('add/', views.add_numbers, name='add_numbers'),
    path('names/', views.name_list, name='name_list'),
]