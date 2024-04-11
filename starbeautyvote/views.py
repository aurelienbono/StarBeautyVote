from django.shortcuts import render
from . import models
from datetime import datetime
from django.shortcuts import redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import os 
import re 
from django.conf import settings

# Create your views here.


def landing(request): 
    return render(request,"pages/index.html")

def competitionLanding(request): 
    context = {} 
    CompetionList = models.Competition.objects.all()
    
    context['CompetionList'] =  CompetionList 
    context['score'] = CompetionList.count()

    return render(request,"pages/application/competition/competitionLandingPage.html",context)

def competitionDetails(request,pk): 
    
    competitionDetails = models.Competition.objects.filter(competitionId = pk)   
    context = {} 
    context['competitionDetails'] =  competitionDetails 
    context['score'] = competitionDetails.count()

    return render(request,"pages/application/competition/competitionDetailPage.html",context)

def dashboardHome(request) : 
    return render(request ,'pages/application/home.html')


def register(request) : 
    if request.method=="POST" : 
        userInfo = [] 
        
        for element in request.POST : 
            userInfo.append(request.POST[element])
        userInfo = userInfo[1:]
        print(userInfo)
        
        
        user = models.User( 
                    fullName =userInfo[0].str.capitalize() , 
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
        
        userInfo = models.User.objects.filter(email=str(email)).values().first()
        userPassword = userInfo['password']
        
        if userInfo and  userPassword == password : 
            return redirect('/apps/')
        else : 
            messages.error(request, 'Invalid username or password!')
            return redirect('/auths/login')
            
    return render(request ,'pages/application/authentication/login.html')




def modify_filename(filename,image_name):
	# Change the filename from a.jpg to ab.jpg
	new_filename = image_name + os.path.splitext(filename)[1]
	return new_filename

def createCompetition(request): 
    if request.method == 'POST' : 
        competititionInfo = [ ] 
        
        for element in request.POST  : 
            competititionInfo.append(request.POST[element])
        competititionInfo = competititionInfo[1:]
        
        print(competititionInfo)
       
        competitionName = ''.join(re.split("[ ]+", competititionInfo[0])) + datetime.now().strftime('%H:%M:%S.%f')[:-7].replace(':','_')

        
        savePath = os.path.join( os.path.join('StarBeautyVote', 'static'),'media')
        savePath = os.path.join(savePath,competitionName)
    
                
        # save filename to db with path 
        competititionUploadFile = request.FILES['image']
        fs = FileSystemStorage(location=savePath)
        new_name = modify_filename(competititionUploadFile.name ,'logo' )
        filename = fs.save(new_name , competititionUploadFile)
   
        imageFinalPath = os.path.join(savePath,new_name)
        
        
        imageFinalPathSplit = imageFinalPath.split(os.sep)[2:]
        imageFinalPath = f'/'.join(imageFinalPathSplit) 
                
        competitition = models.Competition ( 
                        image               = imageFinalPath,
                        competitionName     = competititionInfo[0],
                        dateToStart         = competititionInfo[2],
                        dateToEnd           = competititionInfo[3],
                        description         = competititionInfo[1],
                        category            = competititionInfo[4],
                        CompetitionPrivacy  = competititionInfo[5],
                                           
                    )
        competitition.save()
        
        return redirect('/apps/competitions/listing')
    return render(request , 'pages/application/competition/createcompetition.html')

def competitionListing(request):
    
    if 'delete' in request.POST : 
        pk = request.POST.get('delete') 
        competition = models.Competition.objects.get(competitionId = pk )   
        print(competition , pk)
        competition.delete()
    elif 'update' in request.POST :
        pass 
    
    context = {} 
    CompetionList = models.Competition.objects.all()
    
    context['CompetionList'] =  CompetionList 
    context['score'] = CompetionList.count()


    return render(request,'pages/application/competition/competitionlisting.html', context)


def competitionDashboard(request):
    candidate = []
    if 'create_candidate' in request.POST : 
        for element in request.POST :
            candidate.append(request.POST[element])
        print("*"*20) 
        print(candidate)
    
    all_candidate   = models.Candidates.objects.all() 
    count           = all_candidate.count()
    
    context = {'all_candidate' : all_candidate, "count":count }
        
    return render(request,'pages/application/competition/competitionDashbord.html',context) 




def recoverPassword(request) : 
    
    return render(request ,'pages/application/authentication/recover.html')


def reset(request) : 
        return render(request ,'pages/application/authentication/reset.html')