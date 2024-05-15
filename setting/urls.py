"""
URL configuration for setting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    
    #pages 
    
    path('admin/', admin.site.urls),
    path('', include('starbeautyvote.urls')), 
    path('landing/', include('starbeautyvote.urls')),
    path('contact/', include('starbeautyvote.urls')), 
    path('blogs/', include('starbeautyvote.urls')), 
    path('faq/', include('starbeautyvote.urls')), 
    path('services/', include('starbeautyvote.urls')), 
    path('support/', include('starbeautyvote.urls')), 
    path('pricing/', include('starbeautyvote.urls')), 
    path('detailsBlogs/<str:pk>/', include('starbeautyvote.urls')),   
    path('competitionLanding/', include('starbeautyvote.urls')),
    path('competitionDetails/', include('starbeautyvote.urls')),
    
    # dashboard 
    path('apps/', include('starbeautyvote.urls')), 
    path('auths/register/', include('starbeautyvote.urls')), 
    path('auths/login/', include('starbeautyvote.urls')), 
    path('auths/reset/', include('starbeautyvote.urls')),
    path('apps/competitions/candi/<str:pk>/', include('starbeautyvote.urls')),
    
    
    #Candi 
    path('auths/candi/register/', include('starbeautyvote.urls')), 
    path('apps/candi/profile', include('starbeautyvote.urls')), 
    
    
    # auth 
    path('auths/recoverPassword/', include('starbeautyvote.urls')),
    path('apps/competitions/create', include('starbeautyvote.urls')), 
    path('apps/competitions/dashboard', include('starbeautyvote.urls')),
    
    #Account 
    path('apps/pricing/', include('starbeautyvote.urls')),
    path('apps/accountBuilding/', include('starbeautyvote.urls')),
    path('apps/parameters/', include('starbeautyvote.urls')),
    
    #Payment
    path('checkoutpayment/candi/<str:pk>/', include('starbeautyvote.urls')),
    path('errorpayment/candi/', include('starbeautyvote.urls')),
    path('successpayment/candi/', include('starbeautyvote.urls')),


    
]
