from django.urls import path, re_path
from .views import *

urlpatterns = [
    
    path('home/', Home.as_view(), name='home_dashboard'),

    path('delete/<int:id>/', deletetask ,name='delete-task'),
    path('multi-delete/', deleteSelected, name="delete-multi-tasks"),

]
