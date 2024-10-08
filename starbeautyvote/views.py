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
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.utils import timezone
import csv
from django.http import HttpResponse
# Create your views here.



## DASHBOARD 

def dashboardHome(request) : 
    
    if 'delete' in request.POST : 
        pk = request.POST.get('delete') 
        competition = models.Competition.objects.get(competitionId = pk )   
        
        folderCompetition = models.Competition.objects.filter(competitionId = pk ).values('image').first()

        folderCompetition = os.path.join( os.path.join('StarBeautyVote', 'static'),'media',folderCompetition['image'].split('/')[1])
        
        try : 
            all_candidate_of_this_competitition = models.Candidates.objects.get(id_competition = pk)
            all_candidate_of_this_competitition.delete()    
        except Exception as e : 
            pass
        
        shutil.rmtree(folderCompetition)
        
        competition.delete()
        
        
        
        
    elif 'update' in request.POST :
        pass 
    
    context = {} 
    CompetionList = models.Competition.objects.filter(id_promoter=request.session.get('userId') ).values()
  
    context['CompetionList'] =  CompetionList 
    context['score'] = CompetionList.count()
    context['userId'] = request.session.get('userId')
    context['fullName'] = request.session.get('fullName')
    context['status'] = request.session.get('status')

    
    context['total_amount'] = Starbeautyvote.get_total_of_amount_promoter(request.session.get('userId'))
    context['modePaymentList']  = models.PaymentMethod.objects.filter(promoterId=request.session.get('userId')).values()
  

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
    context['status'] = request.session.get('status')

    
    context['total_amount'] = Starbeautyvote.get_total_of_amount_promoter(request.session.get('userId'))
    context['modePaymentList']  = models.PaymentMethod.objects.filter(promoterId=request.session.get('userId')).values()
  

    return render(request , 'pages/application/competition/createcompetition.html',context)


def createCandidate(request, pk): 
    if request.method == 'POST': 
        print(request.POST)
        
        media_path = models.Competition.objects.filter(competitionId=pk).values('image').first()
        print(media_path) 
        candidateName = ''.join(re.split("[ ]+", request.POST["fullname"])) +  datetime.now().strftime('%d-%m-%Y').replace('-','_')

        savePath = os.path.join( os.path.join('StarBeautyVote', 'static'),'media',media_path['image'].split('/')[1],candidateName )
    

        print(request.FILES['image'] , candidateName ,savePath )
                
        # # save filename to db with path 
        candidateUploadFile = request.FILES['image']
        fs = FileSystemStorage(location=savePath)
        new_name = Starbeautyvote.modify_filename(candidateUploadFile.name ,'CandidateFullImage' )
        filename = fs.save(new_name , candidateUploadFile)
   
        imageFinalPath = os.path.join(savePath,new_name)
        
        imageFinalPathSplit = imageFinalPath.split(os.sep)[2:]
        imageFinalPath = f'/'.join(imageFinalPathSplit)
        
        
        competition_instance = models.Competition.objects.get(competitionId=pk)
        price_competition = competition_instance.registration_fee
        id_candidate = Starbeautyvote.generate_random_string()
        candidate = models.Candidates( 
                    candidatesId       = id_candidate,  
                    fullName           = request.POST["fullname"].capitalize() , 
                    email              = request.POST["email"], 
                    description        = request.POST["description"],
                    age                = request.POST["age"],
                    numberPhone        = request.POST["phone"],
                    academic_level     = request.POST["academic_level"],
                    profession         = request.POST["profession"],
                    country            = request.POST["country"],
                    city               = request.POST["city"],
                    city_of_origin     = request.POST["city_of_origin"],
                    password           = '1234567@',
                    dataOfRegistration = datetime.now(),
                    image              = imageFinalPath,
                    registration_fee_paid = int(price_competition), 
                    registration_fee_type = 'promoter_free', 
                    registration_fee_status   = 'Paid', 
                    created_by         = 'promoter', 
                    id_competition     = competition_instance,
                    )
        
        candidate.save()
        
        return redirect(f"/apps/competitions/dashboard/{pk}/")
    
    context = {} 
    context['userId'] = request.session.get('userId')
    context['competitionId'] =pk
    context['fullName'] = request.session.get('fullName')
    context['status'] = request.session.get('status')
    
    
    context['total_amount'] = Starbeautyvote.get_total_of_amount_promoter(request.session.get('userId'))
    context['modePaymentList']  = models.PaymentMethod.objects.filter(promoterId=request.session.get('userId')).values()
    
    return render(request, 'pages/application/competition/candidatecreate.html',context)

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
    context['status'] = request.session.get('status')

    # # get all information about vote and money 
    
    context['total_votes'] = models.Votes.objects.filter(id_competition=pk).aggregate(total_votes=Sum('numberOfVote'))['total_votes']
    context['total_price'] = models.Votes.objects.filter(id_competition=pk).aggregate(total_price=Sum('priceVoter'))['total_price']

    # percentage calculate  for price 
    
    current_week =  Starbeautyvote.get_total_performance_for_week(pk,'total_price',perfomance_type='competition' , week='current')
    last_week =     Starbeautyvote.get_total_performance_for_week(pk,'total_price', perfomance_type='competition' , week='last')
    context['priceVoterCalculate'], context['priceVoterCalculate_status'] = Starbeautyvote.percentageCalculate(last_week,current_week)
    
    # percentage calculate  for votes 
    
    current_week_vote =  Starbeautyvote.get_total_performance_for_week(pk,'total_votes',perfomance_type='competition' , week='current')
    last_week_vote =     Starbeautyvote.get_total_performance_for_week(pk,'total_votes',perfomance_type='competition' , week='last')
    context['numberOfVoteCalculate'], context['numberOfVoteCalculate_status'] = Starbeautyvote.percentageCalculate(last_week_vote,current_week_vote)
    
    # percentage calculate  for price 
    
    current_week_candi =  Starbeautyvote.get_total_performance_of_candidate_for_week(pk, week='current')
    last_week_candi    =     Starbeautyvote.get_total_performance_of_candidate_for_week(pk, week='last')    
    context['numberOfCandidateCalculate'], context['numberOfCandidateCalculate_status'] = Starbeautyvote.percentageCalculate(last_week_candi,current_week_candi)
    

    
    # # get registration_fee of this competition
    competitionDetails             =  models.Competition.objects.filter(competitionId = pk).values().first()

    context['competitionDetails']  =  competitionDetails
    context['userId'] = request.session.get('userId')
    context['fullName'] = request.session.get('fullName')
    context['competitionId'] = pk
    
    context['total_amount'] = Starbeautyvote.get_total_of_amount_promoter(request.session.get('userId'))
    context['modePaymentList']  = models.PaymentMethod.objects.filter(promoterId=request.session.get('userId')).values()
    
    context['total_registration_fee'] = models.Candidates.objects.filter(id_competition_id=pk).aggregate(total_registration_fee=Sum('registration_fee_paid'))['total_registration_fee']

    context["base_url"] = request.build_absolute_uri('/')[:-1]
    
    return render(request,'pages/application/competition/competitionDashbord.html',context) 



def competitionCandidateProfile(request,pk): 
    
    if 'Download_csv' in  request.POST : 
        candidates_with_votes = models.Votes.objects.filter(id_candidates = pk).values()
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="starbeautyvote_competitions.csv"'
        writer = csv.writer(response)
        
        writer.writerow(['voteId', 'numberOfVote', 'priceVoter', 'vote_type'])
        for candidate in candidates_with_votes:
            writer.writerow([candidate['voteId'], candidate['numberOfVote'], candidate['priceVoter'], candidate['vote_type']])
            
            
        print("Download ok")
        
        return response
    
    
    if "freevote" in request.POST : 
        name  = request.POST.get('name')
        votesNumber  = request.POST.get('votes')
        candidate_id  = request.POST.get('candidate_id')
        
        
        print(name , votesNumber, candidate_id)
        
        priceAmout = Starbeautyvote.voteNumberToFinalAmount(votesNumber)
        phone_queryset  = models.Promoter.objects.filter(promoterId = request.session.get('userId')).values('numberPhone')
        phone_numbers = [entry['numberPhone'] for entry in phone_queryset]
        id_competition_dict = models.Candidates.objects.filter(candidatesId = pk).values('id_competition_id').first()
        id_candidate_instance = models.Candidates.objects.get(candidatesId = pk)
        
        
        if id_competition_dict:
            id_competition_id = id_competition_dict['id_competition_id']
            id_competition_instance = models.Competition.objects.get(competitionId = id_competition_id)
        else:
            id_competition_id = None 
       
        votes = models.Votes ( 
                                voteId = Starbeautyvote.generate_random_string(), 
                                id_competition = id_competition_instance, 
                                id_candidates =id_candidate_instance , 
                                nameVoter =name , 
                                numberPhoneVoter =phone_numbers[0] , 
                                numberOfVote =int(votesNumber) , 
                                priceVoter = priceAmout, 
                                dataOfVoting = datetime.now(),
                                status = 'Success', 
                                voted_by = 'Promoter', 
                                reasonForVote = 'Reel', 
                                vote_type = 'promoter_free'
                                
                        )
        votes.save()
      
    
      
      # paid vote for promoter   
        
    if "paidvote" in request.POST : 
        name  = request.POST.get('name')
        votesNumber  = request.POST.get('votes')
        candidate_id  = request.POST.get('candidate_id')
        
        priceAmout = Starbeautyvote.voteNumberToFinalAmount(votesNumber)
        phone_queryset  = models.Promoter.objects.filter(promoterId = request.session.get('userId')).values('numberPhone')
        phone_numbers = [entry['numberPhone'] for entry in phone_queryset]
        id_competition_dict = models.Candidates.objects.filter(candidatesId = pk).values('id_competition_id').first()
        id_candidate_instance = models.Candidates.objects.get(candidatesId = pk)
        
        if id_competition_dict:
            id_competition_id = id_competition_dict['id_competition_id']
            id_competition_instance = models.Competition.objects.get(competitionId = id_competition_id)
        else:
            id_competition_id = None 
            
        
        try : 
            response , reference = Payments.initialisePayment(priceAmout)
      
        except Exception as  exceptionInitPayment : 
            print(exceptionInitPayment)
            
            messages.error(request, 'Transaction failed: We would like to inform you that the votes have been successfully paid. Thank you for your cooperation and trust.')
            return redirect(f'/apps/competitions/candi/{pk}/')
        
        try : 
            response_result = Payments.completePayment(reference)
      
        except Exception as  exceptionCompletePayment : 
            print(exceptionCompletePayment)
        
            
            messages.error(request, 'Transaction failed: We would like to inform you that the votes have been successfully paid. Thank you for your cooperation and trust.')
            return redirect(f'/apps/competitions/candi/{pk}/')
        
        votes = models.Votes( 
                                voteId = Starbeautyvote.generate_random_string(), 
                                id_competition = id_competition_instance, 
                                id_candidates =id_candidate_instance , 
                                nameVoter =name , 
                                numberPhoneVoter =phone_numbers , 
                                numberOfVote =int(votesNumber) , 
                                priceVoter = priceAmout, 
                                dataOfVoting = datetime.now(),
                                status = 'Success',
                                voted_by = 'Promoter', 
                                reasonForVote = 'Reel', 
                                vote_type = 'promoter_paid'
                                
                        )
        votes.save()
        
        transaction = models.Transaction( 
                                              transactionId = Starbeautyvote.generate_random_string(), 
                                              amount = priceAmout, 
                                              payment_method = 'Mobile Money' , 
                                              status = 'Complete', 
                                              created_at = datetime.now(), 
                                              updated_at = datetime.now(), 
                                              transaction_type = "VoteTransactionByPromoter", 
                                          
                                                 )
                
        transaction.save()
        
        # update balance of promoter
        
        try:
            promoter = models.Promoter.objects.get(promoterId=request.session.get('userId'))
            promoter.balance  += priceAmout 
            promoter.save()
            

        except models.Promoter.DoesNotExist:
            # Managing the case where the promoter does not exist
            print("Promoter not found")
        
        messages.success(request, 'Transcation Accept :  We would like to inform you that the votes have been successfully paid. Thank you for your cooperation and trust.')
        return redirect(f'/apps/competitions/candi/{pk}/')
    
    if "pumpingup" in request.POST : 
        name  = request.POST.get('name')
        votesNumber  = request.POST.get('votes')
        candidate_id  = request.POST.get('candidate_id')
        
        
        print(name , votesNumber, candidate_id)
        
        priceAmout = Starbeautyvote.voteNumberToFinalAmount(votesNumber)
        phone_queryset  = models.Promoter.objects.filter(promoterId = request.session.get('userId')).values('numberPhone')
        phone_numbers = [entry['numberPhone'] for entry in phone_queryset]
        id_competition_dict = models.Candidates.objects.filter(candidatesId = pk).values('id_competition_id').first()
        id_candidate_instance = models.Candidates.objects.get(candidatesId = pk)
        
        
        if id_competition_dict:
            id_competition_id = id_competition_dict['id_competition_id']
            id_competition_instance = models.Competition.objects.get(competitionId = id_competition_id)
        else:
            id_competition_id = None 
       
        votes = models.Votes ( 
                                voteId = Starbeautyvote.generate_random_string(), 
                                id_competition = id_competition_instance, 
                                id_candidates =id_candidate_instance , 
                                nameVoter =name , 
                                numberPhoneVoter =phone_numbers[0] , 
                                numberOfVote =int(votesNumber) , 
                                priceVoter = priceAmout, 
                                dataOfVoting = datetime.now(),
                                status = 'Success',
                                voted_by = 'Promoter', 
                                reasonForVote = 'Pumping up', 
                                vote_type = 'pumpingup' 
                                
                        )
        votes.save()
    
            
    candidateDetails = models.Candidates.objects.filter(candidatesId = pk)   
    
    context = {} 
    # get information about 
    context['candidates_with_votes'] = models.Votes.objects.filter(id_candidates = pk).values()
    context['total_price'] = models.Votes.objects.filter(id_candidates=pk).aggregate(total_price=Sum('priceVoter'))['total_price']
    context['total_votes'] = models.Votes.objects.filter(id_candidates=pk).aggregate(total_votes=Sum('numberOfVote'))['total_votes']

    context['fullName'] = request.session.get('fullName')
    context['status'] = request.session.get('status')
  
    context['candidateDetails'] =  candidateDetails 
    context['score'] = candidateDetails.count()
    
    context['total_amount'] = Starbeautyvote.get_total_of_amount_promoter(request.session.get('userId'))
    context['modePaymentList']  = models.PaymentMethod.objects.filter(promoterId=request.session.get('userId')).values()
    
    
    return render(request, "pages/application/competition/candidateProfile.html",context)



def condidateProfile(request): 
    context = {}
    context['fullName'] = request.session.get('fullName')[0]
    context['image'] = request.session.get('image')[0]
    context['idCandidate'] = request.session.get("idCandidate")[0]
    context['status'] = request.session.get("status")    

    
    # get information about sur le candidate
    candidateDetails  = models.Candidates.objects.filter(candidatesId = context['idCandidate'] ).values().first()
    context['total_price'] = models.Votes.objects.filter(id_candidates=context['idCandidate']).aggregate(total_price=Sum('priceVoter'))['total_price']
    context['total_votes'] = models.Votes.objects.filter(id_candidates=context['idCandidate']).aggregate(total_votes=Sum('numberOfVote'))['total_votes']
    
    
    # percentage calculate  for price 
    
    current_week =  Starbeautyvote.get_total_performance_for_week(context['idCandidate'],'total_price', week='current')
    last_week =     Starbeautyvote.get_total_performance_for_week(context['idCandidate'],'total_price', week='last')
    context['priceVoterCalculate'], context['priceVoterCalculate_status'] = Starbeautyvote.percentageCalculate(last_week,current_week)
    
    # percentage calculate  for votes 
    
    current_week_vote =  Starbeautyvote.get_total_performance_for_week(context['idCandidate'],'total_votes', week='current')
    last_week_vote =     Starbeautyvote.get_total_performance_for_week(context['idCandidate'],'total_votes', week='last')
    context['numberOfVoteCalculate'], context['numberOfVoteCalculate_status'] = Starbeautyvote.percentageCalculate(last_week_vote,current_week_vote)

    

    # candidate_instance = models.Candidates.objects.get(candidatesId=context['idCandidate'])
    
    context['votes_candidate_info'] = models.Votes.objects.filter(id_candidates=context['idCandidate'] ).values()

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
                    dataOfRegistration= datetime.now(),
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
            request.session['status'] = 'promoter'
            
            
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
                    registration_fee_status   = 'UnPaid', 
                    created_by         = 'Candidate', 
                    id_competition     = competition_instance,
                    )
        
        candidate.save()
        
        request.session['fullName'] =  candidateInfo[0].capitalize() , 
        request.session['image']    = imageFinalPath , 
        request.session['idCandidate'] =  id_candidate , 
        request.session['status']      = 'candidate'
        
   
        
        
        if price==0 : 
            # redirect to candidate DashBoard
            updateCandidateRegisterFee = models.Candidates.objects.get(candidatesId =id_candidate)
            updateCandidateRegisterFee.registration_fee_status = "Paid"
            updateCandidateRegisterFee.save()
            return redirect('/apps/candi/profile')
        else : 
            # redirect to pay page
            return redirect(f'/checkoutpayment/candi/{pk}/{id_candidate}/{price}')

    
    return render(request, 'pages/application/authentication/candidate/register.html', {'competition_id': pk, 'registration_fee':price})


def recoverPassword(request) : 
    
    return render(request ,'pages/application/authentication/recover.html')


def reset(request) : 
    return render(request ,'pages/application/authentication/reset.html')
    


# PAGES 

def landing(request): 
    return render(request,"pages/index.html")

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
                                voted_by = 'public', 
                                reasonForVote = 'Reel', 
                                vote_type = 'public_paid'
                                
                        )
        votes.save()
        
        transaction = models.Transaction( 
                                              transactionId = Starbeautyvote.generate_random_string(), 
                                              amount = priceAmout, 
                                              payment_method = 'Mobile Money' , 
                                              status = 'Complete', 
                                              created_at = datetime.now(), 
                                              updated_at = datetime.now(), 
                                              transaction_type = "VoteTransaction", 
                                              
                                                 )
        transaction.save()
        
        
        # update balance of promoter
        competition = models.Competition.objects.get(competitionId=pk)
        promoterId = competition.id_promoter_id

        try:
            promoter = models.Promoter.objects.get(promoterId=promoterId)
            promoter.balance  += priceAmout
            promoter.save()
        except models.Promoter.DoesNotExist:
            # Managing the case where the promoter does not exist
            print("Promoter not found")
                
        

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

def checkoutPayment(request, pk, candi_pk,  price):
    
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

            payment_price = request.POST.get('price')
            # payment_pk = pk
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
                
                transaction = models.Transaction( 
                                              transactionId = Starbeautyvote.generate_random_string(), 
                                              amount = payment_price, 
                                              payment_method = 'Mobile Money' , 
                                              status = "Complete", 
                                              created_at =datetime.now(),
                                              updated_at =datetime.now(),
                                              transaction_type = "CompetitionFee", 
                                              
                                                 )
                
                transaction.save()
                
                 # Update status payment inscription status 
                
                updateCandidateRegisterFee = models.Candidates.objects.get(candidatesId =candi_pk)
                updateCandidateRegisterFee.registration_fee_status = "Paid"
                updateCandidateRegisterFee.registration_fee_paid = int(payment_price)
                updateCandidateRegisterFee.save() 

                
          
                candidate = models.Candidates.objects.get(candidatesId=candi_pk)
                competition_id = candidate.id_competition_id

                competition = models.Competition.objects.get(competitionId=competition_id)
                promoter_id = competition.id_promoter_id

                try:
                    promoter = models.Promoter.objects.get(promoterId=promoter_id)
                    promoter.balance  += int(payment_price)
                    promoter.save()
                
                except models.Promoter.DoesNotExist:
                    # Managing the case where the promoter does not exist
                    print("Promoter not found")
           
                
        
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



## SETTINGS

def parameters(request):
    context = {} 
    context['userId'] = request.session.get('userId')
    context['fullName'] = request.session.get('fullName')
    context['status'] = request.session.get('status')

    
    
    context['total_amount'] = Starbeautyvote.get_total_of_amount_promoter(request.session.get('userId'))
    context['modePaymentList']  = models.PaymentMethod.objects.filter(promoterId=request.session.get('userId')).values()
    
    
    return render(request,'pages/application/account/settings.html',context )


def pricing(request): 
    context = {} 
    context['userId'] = request.session.get('userId')
    context['fullName'] = request.session.get('fullName')
    context['status'] = request.session.get('status')

    context['total_amount'] = Starbeautyvote.get_total_of_amount_promoter(request.session.get('userId'))
    context['modePaymentList']  = models.PaymentMethod.objects.filter(promoterId=request.session.get('userId')).values()
    
    
    return render(request,'pages/application/account/pricing.html',context )


def accountBuilding(request): 
    
    
    id_promoter_instance = models.Promoter.objects.get(promoterId = request.session.get('userId'))
    if "savingnumber" in request.POST  : 
        print(request.POST)
        
        

        typePayment = models.PaymentMethod( 
                                            PaymentMethodId = Starbeautyvote.generate_random_string(),
                                            name            = request.POST['fullName'],
                                            typeOfMethode   = request.POST['typeOfTransfert'],
                                            phoneNumber     = request.POST['phone'],
                                            is_active       = 'True',
                                            created_at      = datetime.now(),
                                            updated_at      = datetime.now(),
                                            promoterId      = id_promoter_instance
                                            )
        
        typePayment.save()
    
    if "launchtransfer" in request.POST: 
        name            = request.session.get('fullName')
        phoneNumber   = request.POST['phoneNumber']
        amout     = int(request.POST['amount'])
        
        totalAmout = Starbeautyvote.get_total_of_amount_promoter(request.session.get('userId'))
        
        if 400 <= amout <= totalAmout:
            # launch payment
            
            try : 
                result, result_status = Payments.launchTransfert(Starbeautyvote.generate_random_string())
                if result_status =='Accepted' : 
                    try:
                        promoter = models.Promoter.objects.get(promoterId=request.session.get('userId'))
                        promoter.balance  -= int(amout)
                        promoter.save()
                        print("Promoter  ok")
                        transaction = models.Transaction( 
                                              transactionId = Starbeautyvote.generate_random_string(), 
                                              amount = amout, 
                                              payment_method = 'Mobile Money' , 
                                              status = 'Complete', 
                                              created_at = datetime.now(), 
                                              updated_at = datetime.now(), 
                                              transaction_type = "PromoterTransfer", 
                                              
                                                 )
                        transaction.save()
                        
                        transfer = models.Transfer( 
                                                      transferId = Starbeautyvote.generate_random_string(), 
                                                      promoterId = promoter,
                                                      amount = int(amout),
                                                      transfer_date = datetime.now(), 
                                                      status = "COMPLETED", 
                                                      bank_account = phoneNumber
                                                      )
                        transfer.save()
                        
                    
                    except models.Promoter.DoesNotExist:
                        # Managing the case where the promoter does not exist
                        print("Promoter not found") 

                else : 
                    messages.error(request, 'Dear user We have encountered an error, please revalidate the transfer. ')
                    return redirect('/apps/accountBuilding/')
                    
                    
                    
            except Exception as e : 
                messages.error(request, 'Dear user We have encountered an error, please revalidate the transfer. ')
                return redirect('/apps/accountBuilding/')
                
            print("launch payment")
            pass 
        
        else : 
            messages.error(request, 'The amount you wish to transfer is below the minimum required to complete a transaction. Please check your balance and carry out a new validation for transfers of 400 FCFA or more.')
            return redirect('/apps/accountBuilding/')
        
         
    
    
    if "deleteModePayment" in request.POST : 
        # print(request.POST)
        # if request.POST['fullname'] : 
        #     pk = request.POST.get('deleteModePayment')
        #     typePayment_value = models.PaymentMethod.objects.get(PaymentMethodId = pk) 
        #     typePayment_value.delete()
        
        pass
        
    
    context = {} 
    context['userId'] = request.session.get('userId')
    context['fullName'] = request.session.get('fullName')
    context['status'] = request.session.get('status')
 
    
    
    
    context['total_amount'] = Starbeautyvote.get_total_of_amount_promoter(request.session.get('userId'))
    context['modePaymentList']  = models.PaymentMethod.objects.filter(promoterId=request.session.get('userId')).values()
    
    return render(request,'pages/application/account/accountBilling.html',context )


def paymentHistorique(request): 
    
    if 'Download_csv' in  request.POST : 
        transfertHistorique = models.Transfer.objects.filter(promoterId = request.session.get('userId')).values()
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="starbeautyvote_Transfer.csv"'
        writer = csv.writer(response)
        
        writer.writerow(['transferId', 'promoterId', 'amount', 'transfer_date','status','bank_account'])
        for transfert in transfertHistorique:
            writer.writerow([transfert['transferId'], transfert['promoterId'], transfert['amount'], transfert['transfer_date'], transfert['status'], transfert['bank_account']])
            
            
        print("Download ok")
        
        return response
    
    context = {} 
    context['userId'] = request.session.get('userId')
    context['fullName'] = request.session.get('fullName')
    context['status'] = request.session.get('status')

    
    id_promoter_instance = models.Promoter.objects.get(promoterId = request.session.get('userId'))
    
    context['total_amount'] = Starbeautyvote.get_total_of_amount_promoter(request.session.get('userId'))
    context['modePaymentList']  = models.PaymentMethod.objects.filter(promoterId=request.session.get('userId')).values()
    
    
    context['transfertHistorique'] = models.Transfer.objects.filter(promoterId = request.session.get('userId')).values()
    return render(request,'pages/application/account/paymentHistory.html',context )



def orderDescription(request) : 
    context = {} 
    context['userId'] = request.session.get('userId')
    context['fullName'] = request.session.get('fullName')
    context['status'] = request.session.get('status')

    
    manager = Starbeautyvote()
    context['total_amount'] = Starbeautyvote.get_total_of_amount_promoter(request.session.get('userId'))
    context['modePaymentList']  = models.PaymentMethod.objects.filter(promoterId=request.session.get('userId')).values()
    
    context['competition_details'], context['competition_registration_details'], context['all_competition_all_details'] = manager.get_competition_info_promoter(request.session.get('userId'))

    context['range'] =list( range(10))
    return render(request,'pages/application/account/orderDescription.html',context )


def contact(request): 
    if request.method=="POST":
        # SAVE DATA IN DATABASE 
        support = models.Supports( 
                        supportId = Starbeautyvote.generate_random_string(),
                        fistName = request.POST['firstname'], 
                        lastName = request.POST['lastname'], 
                        emails  = request.POST['email'], 
                        phone = request.POST['phone'], 
                        subject   = request.POST['subject'], 
                        messages = request.POST['messages'], 
                        created_at = datetime.now(),
                        )

        support.save()
        
        destinataires = ['bonombelleaurelien08@gmail.com']
        # SEND EMAIL 
        
        try: 
            send_mail(request.POST['subject'], request.POST['messages'],  request.POST['email'], destinataires )
            messages.success(request, f'{e}')
        except Exception as e : 
            messages.error(request, f'{e}')
            pass
        
        return redirect('/contact/#sct_contact_form')
        
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