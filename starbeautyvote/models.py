from django.db import models
import uuid
# Create your models here.

class Promoter(models.Model)  : 
    promoterId      = models.CharField(primary_key=True,max_length=50, unique=True)
    fullName    = models.CharField(max_length=50)
    email       = models.EmailField(max_length=50,unique=True)
    numberPhone = models.CharField(max_length=15)
    password    = models.CharField(max_length=24)
    position    = models.CharField(max_length=25)
    dataOfRegistration = models.DateField(auto_now=True)

        
class Competition(models.Model): 
    competitionId        = models.CharField(primary_key=True,max_length=50, unique=True)
    image                = models.ImageField()
    competitionName      = models.CharField(max_length=50)
    dateToStart          = models.DateField()
    dateToEnd            = models.DateField()
    description          = models.TextField()
    category             = models.CharField(max_length=50)
    CompetitionPrivacy   = models.CharField(max_length=20)
    registration_fee     = models.IntegerField()
    id_promoter          = models.ForeignKey(Promoter, on_delete=models.CASCADE)
    

class Candidates(models.Model) : 
    candidatesId                = models.CharField(primary_key=True,max_length=50, unique=True)
    fullName                    = models.CharField(max_length=50) 
    email                       = models.EmailField(max_length=50,unique=True)
    age                         = models.IntegerField()
    numberPhone                 = models.CharField(max_length=15)
    academic_level              = models.CharField(max_length=50)
    profession                  = models.CharField(max_length=50)   
    country                     = models.CharField(max_length=15, default='Cameroon')
    city                        = models.CharField(max_length=15)
    city_of_origin              = models.CharField(max_length=100, default='Douala')
    dataOfRegistration          = models.DateField(auto_now=True)
    image                       = models.ImageField()
    registration_fee_status     = models.CharField(max_length=20)
    description                 = models.TextField()
    password                    = models.CharField(max_length=24)
    id_competition              = models.ForeignKey(Competition , on_delete=models.CASCADE)
     


