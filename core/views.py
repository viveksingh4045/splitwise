from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import   auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods

# Create your views here.
def index(request):
    
    return render(request, 'my.html')

def signup(request):
    User = get_user_model()
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_no = request.POST['phone']
        password = request.POST['password']
        password2 = request.POST['confirm_password']

        if password == password2:
            if User.objects.filter(email = email).exists():
                messages.info(request, 'Email already exists')
                return redirect('index')
            
            elif User.objects.filter(phone_no = phone_no).exists():
                messages.info(request, 'Phone number already exists')
                return redirect('index')
            else:
                user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name,phone_no=phone_no)
                user.save()

                user_login  = auth.authenticate(username=email, password = password)
                auth.login(request, user_login)
                return redirect('user_created')
        else:
            messages.info(request, "Passowrd not matching")
            return redirect('index')
    else:
        return render(request, 'index.html')
    

def user_created(request):
    return HttpResponse("User Created Successfully")

def user_creation_failed(request):
    return HttpResponse("User Creation failed")

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username and/or Password is invalid')
            return redirect('index')
    return redirect('index')
    
@login_required(login_url='signin')
def dashboard(request):
    User = get_user_model()
    print(request.user)
    user = User.objects.get(email = request.user.email)
    print(f"Username - {user.email}")
    return render(request,'index.html',{"user_det":user})


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('index')
