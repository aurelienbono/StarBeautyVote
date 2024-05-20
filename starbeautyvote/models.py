from django.db import models
import uuid
# Create your models here.

class Promoter(models.Model)  : 
    promoterId         = models.CharField(primary_key=True,max_length=50, unique=True)
    fullName           = models.CharField(max_length=50)
    email              = models.EmailField(max_length=50,unique=True)
    numberPhone        = models.CharField(max_length=15)
    password           = models.CharField(max_length=24)
    position           = models.CharField(max_length=25)
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
    registration_fee_status     = models.CharField(max_length=20 , default='UnPaid')
    description                 = models.TextField()
    password                    = models.CharField(max_length=24)
    id_competition              = models.ForeignKey(Competition , on_delete=models.CASCADE)
     


class Votes(models.Model) : 
    voteId                      = models.CharField(primary_key=True,max_length=50, unique=True)
    id_competition              = models.ForeignKey(Competition , on_delete=models.CASCADE)
    id_candidates               = models.ForeignKey(Candidates , on_delete=models.CASCADE)
    nameVoter                   = models.CharField(max_length=50)
    numberPhoneVoter            = models.CharField(max_length=15)
    numberOfVote                = models.IntegerField()
    priceVoter                  = models.CharField(max_length=50)
    dataOfVoting                = models.DateField(auto_now=True)
    status                      = models.CharField(max_length=50)    


class Transaction(models.Model):
    transactionId     = models.CharField(primary_key=True,max_length=50, unique=True)
    candidateId              = models.ForeignKey(Candidates, on_delete=models.CASCADE, related_name='payments')
    amount            = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method    = models.CharField(max_length=20,)
    status            = models.CharField(max_length=10, default='PENDING')
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)
    transaction_id    = models.CharField(max_length=100, blank=True, null=True)
    transaction_type  = models.CharField(max_length=20,)
    
    
class Notification(models.Model): 
    pass