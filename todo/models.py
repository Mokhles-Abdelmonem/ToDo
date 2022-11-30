from django.db import models
from authentications.models import User
# Create your models here.




class ToDoDate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date =  models.DateField()
    
    def __str__(self):
        return str(self.date)



class TaskGroup(models.Model):
    date =  models.ForeignKey(ToDoDate, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.title




class Task(models.Model):
    group =  models.ForeignKey(TaskGroup, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    important = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)


    def __str__(self):
        return self.text
