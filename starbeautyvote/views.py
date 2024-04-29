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



# Create your views here.


def modify_filename(filename,image_name):
	# Change the filename from a.jpg to ab.jpg
	new_filename = image_name + os.path.splitext(filename)[1]
	return new_filename

def generate_random_string(length=16):
  """
  Generates a random alphanumeric string of specified length.

  Args:
      length (int, optional): The desired length of the random string. Defaults to 10.

  Returns:
      str: A random alphanumeric string.
  """
  chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
  return ''.join(secrets.choice(chars) for _ in range(length))

def landing(request): 
    return render(request,"pages/index.html")


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
        new_name = modify_filename(competititionUploadFile.name ,'competitionLogo' )
        filename = fs.save(new_name , competititionUploadFile)
   
        imageFinalPath = os.path.join(savePath,new_name)
        
        
        imageFinalPathSplit = imageFinalPath.split(os.sep)[2:]
        imageFinalPath = f'/'.join(imageFinalPathSplit) 
        
        # Fetch Promoter instance
        promoter_id = competititionInfo[7]
        promoter_instance = models.Promoter.objects.get(promoterId=promoter_id)
                
        competitition = models.Competition ( 
                        competitionId        = generate_random_string(),                   
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

    # # 
    # # get registration_fee of this competition
    competitionDetails             =  models.Competition.objects.filter(competitionId = pk).values().first()
    
    context['competitionDetails']  =  competitionDetails
    context['userId'] = request.session.get('userId')
    context['fullName'] = request.session.get('fullName')
    
    
        
    return render(request,'pages/application/competition/competitionDashbord.html',context) 


def competitionLanding(request): 
    context = {} 
    CompetionList = models.Competition.objects.all()
    
    context['CompetionList'] =  CompetionList 
    context['score'] = CompetionList.count()

    return render(request,"pages/pages/competitionLandingPage.html",context)


def competitionDetails(request,pk): 
    
    competitionDetails = models.Competition.objects.filter(competitionId = pk)   
    candidateDetails = models.Candidates.objects.filter(id_competition = pk) 
    context = {} 
    context['competitionDetails'] =  competitionDetails 
    context['score'] = candidateDetails.count()
    context['candidateDetails'] =  candidateDetails 

    return render(request,"pages/pages/competitionDetailPage.html",context)


def competitionCandidateProfile(request,pk): 
        
    candidateDetails = models.Candidates.objects.filter(candidatesId = pk)   
    context = {} 
    context['candidateDetails'] =  candidateDetails 
    context['score'] = candidateDetails.count()
    
    return render(request, "pages/application/competition/candidateProfile.html",context)



def register(request) : 
    if request.method=="POST" : 
        userInfo = [] 
        
        for element in request.POST : 
            userInfo.append(request.POST[element])
        userInfo = userInfo[1:]
        
        
        user = models.Promoter( 
                    promoterId        = generate_random_string(),  
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
            if isHasCompetition  : 
                      
                request.session['userId']  = userInfo['promoterId']
                request.session['fullName'] = userInfo['fullName']
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
        new_name = modify_filename(candidateUploadFile.name ,'CandidateFullImage' )
        filename = fs.save(new_name , candidateUploadFile)
   
        imageFinalPath = os.path.join(savePath,new_name)
        
        imageFinalPathSplit = imageFinalPath.split(os.sep)[2:]
        imageFinalPath = f'/'.join(imageFinalPathSplit) 
        
        
        
        #Fetch Promoter instance
        competition_instance = models.Competition.objects.get(competitionId=candidateInfo[10])
        
        candidate = models.Candidates( 
                    candidatesId        = generate_random_string(),  
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
        
        # redirect to candidate DashBoard
        return redirect('/apps/candi/profile')
    
    return render(request, 'pages/application/authentication/candidate/register.html', {'competition_id': pk, 'registration_fee':price})


def checkoutPayment(request,pk):
     
    return render(request,"pages/pages/payments/checkoutPayment.html")


def errorPayment(request,pk): 
    return render(request,"pages/pages/payments/errorPayment.html")


def succesPayment(request,pk): 
    return render(request,"pages/pages/payments/successPayment.html")






def condidateProfile(request): 
    
    return render(request, "pages/application/candidate/profile.html")


def recoverPassword(request) : 
    
    return render(request ,'pages/application/authentication/recover.html')


def reset(request) : 
    return render(request ,'pages/application/authentication/reset.html')
    

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

def parameters(request):
    context = {} 
    context['userId'] = request.session.get('userId')
    context['fullName'] = request.session.get('fullName')
    
    
    return render(request,'pages/application/account/settings.html',context )