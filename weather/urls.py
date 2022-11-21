from django.urls import path
from . import views

# Main url for the home/index, and one extra url path as an api to delete a city from the db

urlpatterns = [
    path('', views.index, name='home'),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
]
