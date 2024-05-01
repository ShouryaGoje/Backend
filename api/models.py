from django.db import models
import random
from datetime import date

def get_id():
    while True:
        id = random.randint(1,10**6 )
        if User.objects.filter(u_id = id).count() == 0:
            break
    
    return id

def get_current_date():
    return date.today()


# Create your models here.
class User(models.Model):
    u_id = models.IntegerField(unique=True,default=get_id)
    username = models.CharField(max_length = 15)
    f_name = models.CharField(max_length = 50)
    l_name = models.CharField(max_length = 50)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    password = models.CharField(max_length = 50)

class Profile(models.Model):
    u_id = models.IntegerField()
    p_id = models.IntegerField(default=get_id,unique=True)
    p_name = models.CharField(max_length = 50)
    p_dob  = models.DateField(auto_now=False, auto_now_add=False)


class GraphDatabase(models.Model):
    u_id = models.IntegerField()
    p_id = models.IntegerField()
    p_name = models.CharField(max_length = 50)
    time_array = models.JSONField()
    volume_array = models.JSONField()
    total_volume = models.FloatField(default=3.1)
    date = models.DateField(default=get_current_date)

    
# class test(models.Model):
#     array = models.JSONField()