from django.shortcuts import render, redirect
from . import models
from datetime import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import os 
import re 
from django.conf import settings
import shutil
import secrets
from .payments import Payments
from .custum import Starbeautyvote 
from django.db.models import Sum



# Create your views here.

def landing(request): 
    return render(request,"pages/index.html")

## DASHBOARD 

def dashboardHome(request) : 
    
    if 'delete' in request.POST : 
        pk = request.POST.get('delete') 
        competition = models.Competition.objects.get(competitionId = pk )   
        
        folderCompetition = models.Competition.objects.filter(competitionId = pk ).values('image').first()

        folderCompetition = os.path.join( os.path.join('StarBeautyVote', 'static'),'media',folderCompetition['image'].split('/')[1])
        
        
        all_candidate_of_this_competitition = models.Candidates.objects.get(id_competition = pk)
        
        shutil.rmtree(folderCompetition)
        all_candidate_of_this_competitition.delete()
        competition.delete()
        
        
    elif 'update' in request.POST :
        pass 
    
    context = {} 
    CompetionList = models.Competition.objects.filter(id_promoter=request.session.get('userId') ).values()
    
    
    
    context['CompetionList'] =  CompetionList 
    context['score'] = CompetionList.count()
    context['userId'] = request.session.get('userId')
    context['fullName'] = request.session.get('fullName')
    
    
  

    return render(request ,'pages/application/home.html',context)


def createCompetition(request): 
    if request.method == 'POST' : 
        competititionInfo = [ ] 
        
        for element in request.POST  : 
            competititionInfo.append(request.POST[element])
        competititionInfo = competititionInfo[1:]
        
        print(competititionInfo)
       
        competitionName = ''.join(re.split("[ ]+", competititionInfo[0])) + datetime.now().strftime('%d-%m-%Y').replace('-','_')

        
        savePath = os.path.join( os.path.join('StarBeautyVote', 'static'),'media',competitionName)
    
                
        # save filename to db with path 
        competititionUploadFile = request.FILES['image']
        fs = FileSystemStorage(location=savePath)
        new_name = Starbeautyvote.modify_filename(competititionUploadFile.name ,'competitionLogo' )
        filename = fs.save(new_name , competititionUploadFile)
   
        imageFinalPath = os.path.join(savePath,new_name)
        
        
        imageFinalPathSplit = imageFinalPath.split(os.sep)[2:]
        imageFinalPath = f'/'.join(imageFinalPathSplit) 
        
        # Fetch Promoter instance
        promoter_id = competititionInfo[7]
        promoter_instance = models.Promoter.objects.get(promoterId=promoter_id)
                
        competitition = models.Competition ( 
                        competitionId        = Starbeautyvote.generate_random_string(),                   
                        image               = imageFinalPath,
                        competitionName     = competititionInfo[0],
                        dateToStart         = competititionInfo[2],
                        dateToEnd           = competititionInfo[3],
                        description         = competititionInfo[1],
                        category            = competititionInfo[4],
                        CompetitionPrivacy  = competititionInfo[5],
                        registration_fee    = competititionInfo[6], 
                        id_promoter         = promoter_instance, 
                                           
                    )
        competitition.save()
        
        return redirect('/apps/')

    context = {} 
    promoterId = request.session.get('userId')
    context['promoterId'] = promoterId
    context['userId'] = request.session.get('userId')
    context['fullName'] = request.session.get('fullName')
    
    
  

    return render(request , 'pages/application/competition/createcompetition.html',context)



def competitionDashboard(request,pk):
    
    if 'delete' in  request.POST : 
        pk_candidate = request.POST.get('delete') 
        candidate = models.Candidates.objects.get(candidatesId = pk_candidate )   
        
        folderCandidate = models.Candidates.objects.filter(candidatesId = pk_candidate).values('image').first()

        folderCandidate = os.path.join( os.path.join('StarBeautyVote', 'static'),'media',folderCandidate['image'].split('/')[1],folderCandidate['image'].split('/')[2])
        
        print(candidate, folderCandidate)
        
        shutil.rmtree(folderCandidate)
        candidate.delete()
        
    #get all candidate of this competition
    all_candidate   = models.Candidates.objects.filter(id_competition = pk).values()
    count           = all_candidate.count()
    
    
    context = {'all_candidate' : all_candidate, "count_candidate":count }
    
    context['fullName'] = request.session.get('fullName')

    # # get all information about vote and money 
    
    context['total_votes'] = models.Votes.objects.filter(id_competition=pk).aggregate(total_votes=Sum('numberOfVote'))['total_votes']
    context['total_price'] = models.Votes.objects.filter(id_competition=pk).aggregate(total_price=Sum('priceVoter'))['total_price']

    # # get registration_fee of this competition
    competitionDetails             =  models.Competition.objects.filter(competitionId = pk).values().first()
    
    context['competitionDetails']  =  competitionDetails
    context['userId'] = request.session.get('userId')
    context['fullName'] = request.session.get('fullName')
    
    
        
    return render(request,'pages/application/competition/competitionDashbord.html',context) 



def competitionCandidateProfile(request,pk): 
        
    candidateDetails = models.Candidates.objects.filter(candidatesId = pk)   
    
    context = {} 
    # get information about 
    context['candidates_with_votes'] = models.Votes.objects.filter(id_candidates = pk).values()
    context['total_price'] = models.Votes.objects.filter(id_candidates=pk).aggregate(total_price=Sum('priceVoter'))['total_price']

    
  
    context['candidateDetails'] =  candidateDetails 
    context['score'] = candidateDetails.count()
    
    return render(request, "pages/application/competition/candidateProfile.html",context)



def condidateProfile(request): 
    context = {}
    context['fullName'] = request.session.get('fullName')[0]
    context['image'] = request.session.get('image')[0]
    context['idCandidate'] = request.session.get("idCandidate")[0]
    
    # get information about sur le candidate
    candidateDetails  = models.Candidates.objects.filter(candidatesId = context['idCandidate'] ).values().first()
    context['total_price'] = models.Votes.objects.filter(id_candidates=context['idCandidate']).aggregate(total_price=Sum('priceVoter'))['total_price']
    context['total_votes'] = models.Votes.objects.filter(id_candidates=context['idCandidate']).aggregate(total_votes=Sum('numberOfVote'))['total_votes']


    context['votes_candidate_info'] = models.Votes.objects.filter(id_competition=context['idCandidate'] )


    context['candidateDetails'] = candidateDetails

    return render(request, "pages/application/candidate/profile.html", context)


## AUTHENTIFICATION 

def register(request) : 
    if request.method=="POST" : 
        userInfo = [] 
        
        for element in request.POST : 
            userInfo.append(request.POST[element])
        userInfo = userInfo[1:]
        
        
        user = models.Promoter( 
                    promoterId        = Starbeautyvote.generate_random_string(),  
                    fullName =userInfo[0].capitalize() , 
                    email=userInfo[1], 
                    numberPhone=userInfo[2],
                    position=userInfo[3],
                    password=userInfo[4],
                    dataOfRegistration=datetime.now(),
                    )
        
        user.save()

        return redirect('/auths/login/')
    return render(request ,'pages/application/authentication/register.html')



def login(request) : 
    if request.method=="POST" : 
        email = request.POST['email']
        password = request.POST['password']
        
        userInfo = models.Promoter.objects.filter(email=str(email)).values().first()
        userPassword = userInfo['password']
        
        
        if userInfo and  userPassword == password : 
            isHasCompetition = models.Competition.objects.filter(id_promoter = userInfo['promoterId'] ).values().first()
            
            request.session['userId']  = userInfo['promoterId']
            request.session['fullName'] = userInfo['fullName']
            
            if isHasCompetition  : 
                return redirect('/apps/') 
            else : 
                return redirect('/apps/competitions/create')
        else : 
            messages.error(request, 'Invalid username or password!')
            return redirect('/auths/login')
            
    return render(request ,'pages/application/authentication/login.html')


def candidate_register(request,pk,price) : 
    if request.method=="POST" : 
        candidateInfo = [] 
        
        for element in request.POST : 
            candidateInfo.append(request.POST[element])
        candidateInfo = candidateInfo[1:]
                
        media_path = models.Competition.objects.filter(competitionId=pk).values('image').first()
        
        candidateName = ''.join(re.split("[ ]+", candidateInfo[0])) +  datetime.now().strftime('%d-%m-%Y').replace('-','_')

        savePath = os.path.join( os.path.join('StarBeautyVote', 'static'),'media',media_path['image'].split('/')[1],candidateName )
    
                
        # # save filename to db with path 
        candidateUploadFile = request.FILES['image']
        fs = FileSystemStorage(location=savePath)
        new_name = Starbeautyvote.modify_filename(candidateUploadFile.name ,'CandidateFullImage' )
        filename = fs.save(new_name , candidateUploadFile)
   
        imageFinalPath = os.path.join(savePath,new_name)
        
        imageFinalPathSplit = imageFinalPath.split(os.sep)[2:]
        imageFinalPath = f'/'.join(imageFinalPathSplit) 
        
        
        
        #Fetch Promoter instance
        competition_instance = models.Competition.objects.get(competitionId=candidateInfo[10])
        id_candidate = Starbeautyvote.generate_random_string()
        candidate = models.Candidates( 
                    candidatesId        = id_candidate,  
                    fullName           = candidateInfo[0].capitalize() , 
                    email              = candidateInfo[1], 
                    description        = candidateInfo[2],
                    age                = candidateInfo[3],
                    numberPhone        = candidateInfo[4],
                    academic_level     = candidateInfo[5],
                    profession         = candidateInfo[6],
                    country            = candidateInfo[7],
                    city               = candidateInfo[8],
                    city_of_origin     = candidateInfo[9],
                    password           = candidateInfo[11],
                    dataOfRegistration = datetime.now(),
                    image              = imageFinalPath, 
                    registration_fee_status   = 'None', 
                    id_competition     = competition_instance,
                    )
        
        candidate.save()
        
        request.session['fullName'] =  candidateInfo[0].capitalize() , 
        request.session['image']    = imageFinalPath , 
        request.session['idCandidate'] =  id_candidate , 
        print(id_candidate)
        
        if price==0 : 
            # redirect to candidate DashBoard
            updateCandidateRegisterFee = models.Candidates.objects.get(candidatesId =id_candidate)
            updateCandidateRegisterFee.registration_fee_status = "Pay"
            updateCandidateRegisterFee.save()
            return redirect('/apps/candi/profile')
        else : 
            # redirect to pay page
            return redirect(f'/checkoutpayment/candi/{pk}/{price}')

    
    return render(request, 'pages/application/authentication/candidate/register.html', {'competition_id': pk, 'registration_fee':price})


def recoverPassword(request) : 
    
    return render(request ,'pages/application/authentication/recover.html')


def reset(request) : 
    return render(request ,'pages/application/authentication/reset.html')
    



## SETTINGS

def parameters(request):
    context = {} 
    context['userId'] = request.session.get('userId')
    context['fullName'] = request.session.get('fullName')
    
    
    return render(request,'pages/application/account/settings.html',context )


# PAGES 


def competitionLanding(request): 
    context = {} 
    CompetionList = models.Competition.objects.all()
    
    context['CompetionList'] =  CompetionList 
    context['score'] = CompetionList.count()

    return render(request,"pages/pages/competitionLandingPage.html",context)


def competitionDetails(request,pk): 
    
    if "initialPayment" in request.POST : 
        votesNumber  = request.POST.get('votes')
        candidate_id  = request.POST.get('candidate_id')
        name  = request.POST.get('name')
        phone  = request.POST.get('phone')
        
        priceAmout = Starbeautyvote.voteNumberToFinalAmount(votesNumber)
        competitionId = models.Competition.objects.get(competitionId = pk)
        candiId       = models.Candidates.objects.get(candidatesId = candidate_id)
        
        try : 
            response , reference = Payments.initialisePayment(priceAmout)
      
        except Exception as  exceptionInitPayment : 
            print(exceptionInitPayment)
            return redirect('/errorpayment/candi/')
        
        try : 
            response_result = Payments.completePayment(reference)
      
        except Exception as  exceptionCompletePayment : 
            print(exceptionCompletePayment)
            
            votes = models.Votes ( 
                                voteId = Starbeautyvote.generate_random_string(), 
                                id_competition = competitionId, 
                                id_candidates =candiId , 
                                nameVoter =name , 
                                numberPhoneVoter =phone , 
                                numberOfVote =int(votesNumber) , 
                                priceVoter = priceAmout, 
                                dataOfVoting = datetime.now(),
                                status = 'UnSuccess', 
                                
                        )
            votes.save()
            return redirect('/errorpayment/candi/', idCompetition = pk)
        
        votes = models.Votes ( 
                                voteId = Starbeautyvote.generate_random_string(), 
                                id_competition = competitionId, 
                                id_candidates =candiId , 
                                nameVoter =name , 
                                numberPhoneVoter =phone , 
                                numberOfVote =int(votesNumber) , 
                                priceVoter = priceAmout, 
                                dataOfVoting = datetime.now(),
                                status = 'Success', 
                                
                        )
        votes.save()
        
        transaction = models.Transaction( 
                                              transactionId = Starbeautyvote.generate_random_string(), 
                                              candidateId = candiId, 
                                              amount = priceAmout, 
                                              payment_method = 'Mobile Money' , 
                                              status = response_result["status"], 
                                              created_at =response["transaction"]["created_at"] , 
                                              updated_at =response["transaction"]["updated_at"] , 
                                              reference_id =response["transaction"]["reference"] , 
                                              transaction_type = "VoteTransaction", 
                                              
                                                 )
                
        transaction.save()
        
        return redirect('/successpayment/candi/')
        
    
        
    competitionDetails = models.Competition.objects.filter(competitionId = pk)   
    candidateDetails = models.Candidates.objects.filter(id_competition = pk) 
    candidates_with_votes = models.Candidates.objects.filter(id_competition = pk).prefetch_related('votes_set').all()
    
    for candidate in candidates_with_votes:
        candidate.total_votes = candidate.votes_set.aggregate(total_votes=Sum('numberOfVote'))['total_votes'] or 0

    
 
    context = {} 
    context['competitionDetails'] =  competitionDetails 
    context['score'] = candidateDetails.count()
    context['candidateDetails'] =  candidateDetails
    context['candidates_with_votes'] =  candidates_with_votes 

    return render(request,"pages/pages/competitionDetailPage.html",context)



## PAYMENT 

def checkoutPayment(request, pk, price):
    
    if request.method == 'POST':
        payment_mobile_money = request.POST.get('paymentMobileMoney')
        payment_credit_card = request.POST.get('paymentCreditCard')
        payment_paypal = request.POST.get('paymentPaypal')

        selected_payments = [payment_mobile_money, payment_credit_card, payment_paypal]
        selected_count = sum(bool(payment) for payment in selected_payments)

        if selected_count > 1:
    
            messages.error(request, 'Please select one payment method only!')
            redirect(f'/checkoutpayment/candi/{pk}/{price}/')
        elif payment_mobile_money:
            # Process mobile money payment
            # Your code for handling mobile money

            payment_price = request.POST.get('price')
            payment_pk = pk
            payment_mobile_money_candidate_name= request.POST.get('candidate_name')
            payment_credit_card_candidate_phone = request.POST.get('candidate_phone')
            
            try : 
                response , reference = Payments.initialisePayment(payment_price)
      
            except Exception as  exceptionInitPayment : 
                print(exceptionInitPayment)
                return redirect('/errorpayment/candi/')
            
            try : 
                response_result = Payments.completePayment(reference)
                
                # save to transaction 
                
                # Update status payment inscription status 
                
                transaction = models.Transaction( 
                                              transactionId = Starbeautyvote.generate_random_string(), 
                                              candidateId = payment_pk, 
                                              amount = payment_price, 
                                              payment_method = 'Mobile Money' , 
                                              status = response_result["status"], 
                                              created_at =response["transaction"]["created_at"] , 
                                              updated_at =response["transaction"]["updated_at"] , 
                                              reference_id =response["transaction"]["reference"] , 
                                              transaction_type = "VoteTransaction", 
                                              
                                                 )
                
                transaction.save()
                
                updateCandidateRegisterFee = models.Candidates.objects.get(candidatesId =payment_pk)
                updateCandidateRegisterFee.registration_fee_status = "Paid"
                updateCandidateRegisterFee.save()
        
            except Exception as  exceptionCompletePayment : 
                print(exceptionCompletePayment)

                return redirect('/errorpayment/candi/', idCompetition = pk)
                        
            return redirect('/apps/candi/profile')
        
        
        elif payment_credit_card:

            # Process credit card payment
            # Your code for handling credit card 
            payment_pk =pk
            payment_price = request.POST.get('price')
            payment_credit_card_cardNumber = request.POST.get('cardNumber')
            payment_credit_card_nameCard= request.POST.get('nameCard')
            payment_credit_card_expiry = request.POST.get('expiry')
            payment_credit_card_cvv= request.POST.get('cvv')
            
            print(payment_credit_card_cardNumber,payment_credit_card_nameCard,payment_credit_card_expiry, payment_credit_card_cvv, payment_pk , payment_price )
            
        elif payment_paypal:
            # Process PayPal payment
            # Your code for handling PayPal payment
            payment_price = request.POST.get('price')
            payment_pk = pk
            payment_paypal_email_paypal= request.POST.get('email_paypal')
            
            print(payment_paypal_email_paypal, payment_pk , payment_price)
            
        else:
            pass
        
        
    content = {}
    content['price'] = price
    content['pk'] = pk
    return render(request,"pages/pages/payments/checkoutPayment.html", content)


def errorPayment(request): 
    return render(request,"pages/pages/payments/errorPayment.html")


def successPayment(request): 
    return render(request,"pages/pages/payments/successPayment.html")


def pricing(request): 
    context = {} 
    context['userId'] = request.session.get('userId')
    context['fullName'] = request.session.get('fullName')
    
    return render(request,'pages/application/account/pricing.html',context )


def accountBuilding(request): 
    context = {} 
    context['userId'] = request.session.get('userId')
    context['fullName'] = request.session.get('fullName')
    
    return render(request,'pages/application/account/accountBilling.html',context )



def contact(request): 
    return render(request,"pages/pages/contact.html" )


def blogs(request): 
    return render(request,"pages/pages/blog.html" )

def detailsBlogs(request,pk): 
    return render(request,"pages/pages/blogArticle.html" )

def faq(request): 
    return render(request,"pages/pages/faq.html" )

def services(request): 
    return render(request,"pages/pages/services.html" )

def support(request): 
    return render(request,"pages/pages/support.html" )

def pricing(request): 
    return render(request,"pages/pages/pricing.html" )