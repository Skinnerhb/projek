from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

def reg(request):
    context = {
        'title':'Register'
        }
    if request.method == 'POST':
        Name = request.POST['nam']
        Surname = request.POST['surnam']
        Username = request.POST['user']
        Email = request.POST['email']
        Password1 = request.POST['passa']
        Password2 = request.POST['passb']
        
        if Password1 == Password2:
            if User.objects.filter(username=Username).exists():
                messages.info(request, 'Username already exists')
                return redirect('/register')
            elif User.objects.filter(email=Email).exists():
                messages.info(request, 'Email already exists')
                return redirect('/register')
            else:
                user = User.objects.create_user(username=Username,password=Password1,email=Email,first_name=Name,last_name=Surname)
                user.save()
                return redirect('/')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('/register')
    else:
        return render(request, 'usercreate/register.html',context)

def log(request):
    context = {
        'title':'Login'
        }
    if request.method == "POST":
        Username = request.POST['user']
        Password = request.POST['pass']
        
        user = auth.authenticate(username=Username,password=Password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/main')
        else:
            messages.info(request, 'Invalid username/password')
            return redirect('/')
        
        
    else:
        return render(request, 'usercreate/login.html',context)
    
def logo(request):
    context = {
        'title':'Login'
        }
    auth.logout(request)
    return render(request, 'usercreate/login.html',context)
