from django.db import models
import uuid
# Create your models here.


class Supports(models.Model): 
    supportId         = models.CharField(primary_key=True,max_length=50, unique=True)
    fistName          = models.CharField(max_length=30,)
    lastName          = models.CharField(max_length=30)
    emails            = models.EmailField(max_length=50)
    phone             = models.CharField(max_length=30)
    subject           = models.CharField(max_length=30)
    messages          = models.TextField()
    created_at        = models.DateTimeField(auto_now_add=True)

class Promoter(models.Model)  : 
    promoterId             = models.CharField(primary_key=True,max_length=50, unique=True)
    fullName               = models.CharField(max_length=50)
    email                  = models.EmailField(max_length=50,unique=True)
    numberPhone            = models.CharField(max_length=15)
    password               = models.CharField(max_length=24)
    position               = models.CharField(max_length=25)
    dataOfRegistration     = models.DateField(auto_now=True)
    balance                = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 


        
class Competition(models.Model): 
    competitionId           = models.CharField(primary_key=True,max_length=50, unique=True)
    image                   = models.ImageField()
    competitionName         = models.CharField(max_length=50)
    dateToStart             = models.DateField()
    dateToEnd               = models.DateField()
    description             = models.TextField()
    category                = models.CharField(max_length=50)
    CompetitionPrivacy      = models.CharField(max_length=20)
    registration_fee        = models.IntegerField()
    id_promoter             = models.ForeignKey(Promoter, on_delete=models.CASCADE)
    

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
    registration_fee_paid       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    registration_fee_status     = models.CharField(max_length=20 , default='UnPaid')
    registration_fee_type       = models.CharField(max_length=15, default='public_paid')
    description                 = models.TextField()
    password                    = models.CharField(max_length=24)
    created_by                  = models.CharField(max_length=24,default='Candidate') 
    id_competition              = models.ForeignKey(Competition , on_delete=models.CASCADE)
     


class Votes(models.Model) : 
    voteId                      = models.CharField(primary_key=True,max_length=50, unique=True)
    id_competition              = models.ForeignKey(Competition , on_delete=models.CASCADE)
    id_candidates               = models.ForeignKey(Candidates , on_delete=models.CASCADE)
    nameVoter                   = models.CharField(max_length=50)
    numberPhoneVoter            = models.CharField(max_length=15)
    numberOfVote                = models.IntegerField()
    priceVoter                  = models.DecimalField(max_digits=10, decimal_places=2) 
    dataOfVoting                = models.DateField(auto_now=True)
    status                      = models.CharField(max_length=50) 
    voted_by                    = models.CharField(max_length=15, default='public')
    reasonForVote               = models.CharField(max_length=15, default='Reel') 
    vote_type                   = models.CharField(max_length=15, default='public_paid')


class Transaction(models.Model):
    transactionId           = models.CharField(primary_key=True,max_length=50, unique=True)
    amount                  = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method          = models.CharField(max_length=20,)
    status                  = models.CharField(max_length=10, default='PENDING')
    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)
    transaction_type        = models.CharField(max_length=20,)


class PaymentMethod(models.Model):
    PaymentMethodId        = models.CharField(primary_key=True,max_length=50, unique=True)
    name                   = models.CharField(max_length=255)
    phoneNumber            = models.CharField(max_length=25,  default='')
    typeOfMethode          = models.CharField(max_length=50)
    is_active              = models.BooleanField(default=True)
    created_at             = models.DateTimeField(auto_now_add=True)
    updated_at             = models.DateTimeField(auto_now=True)
    promoterId             = models.ForeignKey(Promoter, on_delete=models.CASCADE)


class Transfer(models.Model):
    transferId          = models.CharField(primary_key=True, max_length=50, unique=True)
    promoterId            = models.ForeignKey(Promoter, on_delete=models.CASCADE)
    amount              = models.DecimalField(max_digits=10, decimal_places=2)
    transfer_date       = models.DateTimeField(auto_now_add=True)
    status              = models.CharField(max_length=20, default='PENDING')
    bank_account        = models.CharField(max_length=50)

  
    
class NotificationPromoter(models.Model): 
    notificationId         = models.CharField(primary_key=True,max_length=50, unique=True)
    typeOfNotification     = models.CharField(max_length=10, default='PENDING')
    description            = models.TextField()
    created_at             = models.DateTimeField(auto_now_add=True)
    promoterId             = models.ForeignKey(Promoter, on_delete=models.CASCADE)
    
class NotificationCandidate(models.Model): 
    notificationId         = models.CharField(primary_key=True,max_length=50, unique=True)
    typeOfNotification     = models.CharField(max_length=10, default='PENDING')
    description            = models.TextField()
    created_at             = models.DateTimeField(auto_now_add=True)
    candidateId            = models.ForeignKey(Candidates, on_delete=models.CASCADE)
    id_competition         = models.ForeignKey(Competition , on_delete=models.CASCADE)

