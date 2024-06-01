from django.urls import path 
from . import views

urlpatterns = [
    path('',views.landing, name='landing'), 
    path('landing/',views.landing, name='landing'),
    path('contact/',views.contact, name='contact'),
    path('blogs/',views.blogs, name='blogs'),
    path('detailsBlogs/<str:pk>',views.detailsBlogs, name='detailsBlogs'),
    path('support/',views.support, name='support'),
    path('faq/',views.faq, name='faq'),
    path('services/',views.services, name='services'),
    path('pricing/',views.pricing, name='pricing'),
    path('competitionLanding/',views.competitionLanding, name='competitionLanding'),
    path('competitionDetails/<str:pk>',views.competitionDetails, name='competitionDetails'),
    path('apps/', views.dashboardHome , name='home'),
    
    path('auths/register/', views.register , name='register'),
    path('auths/login/', views.login , name='login'),
    path('auths/reset/', views.reset , name='reset'),
    path('auths/recoverPassword/', views.recoverPassword , name='recoverPassword'),
    
    path('auths/candi/register/<str:pk>/<int:price>/', views.candidate_register , name='candidateRegister'),
    path('apps/candi/profile', views.condidateProfile , name='condidateProfile'),
    
    path('apps/competitions/create', views.createCompetition , name='createCompetition'),
    path('apps/competitions/dashboard/<str:pk>/', views.competitionDashboard , name='competitionDashboard'),
    path('apps/competitions/candi/<str:pk>/', views.competitionCandidateProfile , name='competitionCandidateProfile'),
 
    path('apps/pricing/', views.pricing , name='pricing'),
    path('apps/accountBuilding/', views.accountBuilding , name='accountBuilding'),
    path('apps/parameters/', views.parameters , name='settings'),


    path('checkoutpayment/candi/<str:pk>/<str:candi_pk>/<int:price>/', views.checkoutPayment , name='checkoutPayment'),

    path('errorpayment/candi/', views.errorPayment , name='errorPayment'),
    path('successpayment/candi/', views.successPayment , name='successPayment'),


        
]
