from django.shortcuts import render

# Create your views here.


def landing(request): 
    return render(request,"pages/index.html")


def dashboardHome(request) : 
    return render(request ,'pages/application/home.html')