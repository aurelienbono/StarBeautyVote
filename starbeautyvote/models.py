from django.db import models
import uuid
# Create your models here.

class User(models.Model)  : 
    userId      = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    fullName    = models.CharField(max_length=50)
    email       = models.EmailField(max_length=50,unique=True)
    numberPhone = models.CharField(max_length=15)
    password    = models.CharField(max_length=24)
    position    = models.CharField(max_length=25)
    dataOfRegistration = models.DateField(auto_now=True)

        
class Competition(models.Model): 
    competitionId        = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image                = models.ImageField()
    competitionName      = models.CharField(max_length=50)
    dateToStart          = models.DateField()
    dateToEnd            = models.DateField()
    description          = models.TextField()
    category             = models.CharField(max_length=50)
    CompetitionPrivacy   = models.CharField(max_length=20)
    

class Candidates(models.Model) : 
    candidatesId        = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    fullName            = models.CharField(max_length=50) 
    age                 = models.IntegerField()
    email               = models.EmailField(max_length=50,unique=True)
    numberPhone         = models.CharField(max_length=15)
    city                = models.CharField(max_length=15)
    taille              = models.DecimalField(max_digits = 5, decimal_places = 2)
    poids               = models.DecimalField(max_digits = 5, decimal_places = 2)
    Photographies       = models.ImageField()
    etude               = models.CharField(max_length=50)
    profession          = models.CharField(max_length=50)
    description         = models.TextField()
    dataOfRegistration  = models.DateField(auto_now=True)

