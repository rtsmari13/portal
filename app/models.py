import datetime
import random
import string
from django.db import models
import uuid
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import gettext as _

# Create your models here.
def password():
    result = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return str(result)

def otp():
    result = ''.join(random.choices( string.digits, k=4))
    return str(result)

def name():
    total_assessment = Assessment.objects.all().last()

    if total_assessment == None:
        assessment = 'Assessment1'
        return assessment
    
    if total_assessment.id >= 1:
        assessment = 'Assessment' + str(total_assessment.id + 1)
        return assessment
    
class User(models.Model):
    UserName = models.CharField(max_length=100, blank=False, unique=True)
    Email = models.CharField(max_length=50, blank='', unique=True)
    MobileNumber = models.CharField(max_length=15, default='')
    Address = models.CharField(max_length=100, blank='')
    City = models.CharField(max_length=100, default='')
    State = models.CharField(max_length=100, default='')
    Credits = models.IntegerField(default=0)
    primary_colour = models.CharField(max_length=250,blank=True,default="#008D96") 
    secondary_colour = models.CharField(max_length=250,blank=True,default="#c8dddf") 
    master_primary_colour = models.CharField(max_length=250,blank=True,default="#008D96") 
    master_secondary_colour = models.CharField(max_length=250,blank=True,default="#c8dddf") 
    Password = models.CharField(max_length=15, blank=False, default=password)
    otp = models.CharField(max_length=10, default=otp)
    Role = models.CharField(max_length=100, default='Admin')
    REQUIRED_FIELDS = [],
    EMAIL_FIELD = "Email"
    USERNAME_FIELD = 'UserName'
    is_anonymous = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    
    class meta:
        ordering = ['-id']


class Recruiters(models.Model):
    CompanyName = models.CharField(max_length=100, blank=False)
    UserName = models.CharField(max_length=100, blank=False)
    Email = models.CharField(max_length=50, blank='',unique=True)
    MobileNumber = models.CharField(max_length=15, default='')
    Address = models.CharField(max_length=100, blank='')
    City = models.CharField(max_length=100, default='')
    State = models.CharField(max_length=100, default='')
    Credits = models.IntegerField(default=0)
    primary_colour = models.CharField(max_length=250,blank=True,default="#008D96") 
    secondary_colour = models.CharField(max_length=250,blank=True,default="#c8dddf")
    master_primary_colour = models.CharField(max_length=250,blank=True,default="#008D96") 
    master_secondary_colour = models.CharField(max_length=250,blank=True,default="#c8dddf") 
    Password = models.CharField(max_length=15, blank=False, default=password)
    otp = models.CharField(max_length=10, default=otp)
    Role = models.CharField(max_length=50, default='user')
    created_at = models.DateTimeField(default=datetime.datetime.now())
    REQUIRED_FIELDS = [],
    EMAIL_FIELD = "Email"
    USERNAME_FIELD = 'UserName'
    is_anonymous = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    
    class meta:
        ordering = ['-id']

class Assessment(models.Model):
    name = models.CharField(max_length=50, default=name)
    tags = models.CharField(max_length=100,default="")
    description = models.TextField(default="")
    url = models.CharField(max_length=250,null=True,blank=True,default="")
    
        
class Questions(models.Model):
    Assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='Question_list', null=True, blank=True)
    question = models.CharField(max_length=500, null=False, default='')
    option1 = models.CharField(max_length=200, null=False, default='')
    option2 = models.CharField(max_length=200, null=False, default='')
    option3 = models.CharField(max_length=200, null=False, default='')
    option4 = models.CharField(max_length=200, null=False, default='')
    answer = models.CharField(max_length=200, null=False, default='')
    
class Plan(models.Model):
    Title = models.CharField(max_length=100)
    Price = models.IntegerField()
    Features = models.CharField(max_length=100)

class FileUpload(models.Model):
    location = models.CharField(max_length=100) 
    experience = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    file = models.FileField() 
    download_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    
    class meta:
        ordering = ['-id']
        