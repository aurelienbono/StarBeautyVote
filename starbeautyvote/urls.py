from django.urls import path 
from . import views

urlpatterns = [
    path('',views.landing, name='landing'), 
    path('landing/',views.landing, name='landing'),
    path('apps/', views.dashboardHome , name='home'),
    
    path('auths/register/', views.register , name='register'),
    path('auths/login/', views.login , name='login'),
    path('auths/reset/', views.reset , name='reset'),
    path('auths/recoverPassword/', views.recoverPassword , name='recoverPassword'),
    
    
    path('apps/competitions/create', views.createCompetition , name='createCompetition'),
    path('apps/competitions/listing', views.competitionListing , name='competitionListing'),
    path('apps/competitions/dashboard', views.competitionDashboard , name='competitionDashboard'),
    
]
