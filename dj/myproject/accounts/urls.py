from django.urls import path
from .views import register , verify_otp , login , logout , dashboard , set_password , calculator

urlpatterns = [
    path('' , register , name='register'),
    path('verify/' , verify_otp , name='verify_otp'),
    path('set_password/', set_password, name='set_password'),
    path('login/', login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout, name='logout'),
    path('calculator/' , calculator , name='calculator')
]
