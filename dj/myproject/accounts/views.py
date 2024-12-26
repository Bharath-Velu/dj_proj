from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login as auth_login , logout as auth_logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import CustomUser , OTP
import random

def register(request):

    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'register.html', {'error': 'Invalid email format.'})

        if CustomUser.objects.filter(email=email).exists():
            return render(request , 'register.html' , {'error': 'Email is already Registered.'})
        
        user = CustomUser.objects.create_user(
            email=email,
            username= email
        )
        user.save()

        otp_code = str(random.randint(100000 , 999999))
        OTP.objects.create(user=user , otp_code=otp_code)

        send_mail(
            'YOUR OTP CODE',
            f'Your OTP Code is {otp_code}',
            'no-reply@gmail.com',
            [email],
        )
        return redirect('verify_otp')
    return render(request , 'register.html')


def verify_otp(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp')

        otp = OTP.objects.filter(otp_code=otp_code).first()
        if otp and otp.is_valid():
            user = otp.user
            user.is_email_verified = True
            user.save()
            otp.delete()
            
            request.session['verified_user_id'] = user.id
            return redirect('set_password')

        return render(request , 'verify.html' , {'error' : 'Invalid or Expire OTP'})
    
    return render(request , 'verify.html')

def set_password(request):
    if request.method == 'POST':
        user_id = request.session.get('verified_user_id')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request , 'set_password.html' , {'error': 'Passwords do not match.'})
        
        user = CustomUser.objects.get(id = user_id)
        user.password = make_password(password)
        user.save()

        del request.session['verified_user_id']
        return redirect('login')
    
    return render(request , 'set_password.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request , username=email , password=password)

        if user:
            if user.is_email_verified:
                auth_login(request , user)
                return redirect('dashboard')
            return render(request , 'login.html' , {'error' : 'Email Not Verified'})
        return render(request , 'login.html' , {'error' : 'Invalid Email or Password.'})
    return render(request, 'login.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def calculator(request):
    return render(request, 'calculator.html')

def logout(request):
    auth_logout(request)
    return redirect('login')