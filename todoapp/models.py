from django.db import models


# Create your models here.
from django.contrib.auth.models import User

class todo_db(models.Model):
    login_id=models.ForeignKey(User,on_delete=models.CASCADE)
    u_id=models.AutoField(primary_key=True)
    task=models.CharField(max_length=100) # user individual tasks
    tasktimedate=models.CharField(max_length=50)
    status=models.CharField(max_length=50) #for handling the task is "done or not completed"
    priority=models.CharField(max_length=50) #(it handles priority is "High | Medium | Normal")
    email=models.CharField(max_length=100,null=True) # it is just for verification of which user

    # taskdate=models.DateField(auto_now=False, auto_now_add=False)
    # tasktime=models.TimeField(auto_now=False, auto_now_add=False)


