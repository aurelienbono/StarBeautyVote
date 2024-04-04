from django.urls import path 
from . import views

urlpatterns = [
    path('',views.landing, name='landing'), 
    path('landing/',views.landing, name='landing'),
    path('apps/', views.dashboardHome , name='home')
    
]
