from django.contrib import admin
from .models import *

# Register your models here.



admin.site.register(ToDoDate)
admin.site.register(TaskGroup)
admin.site.register(Task)