from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt 
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request,("There was an error in logging in Try Again"))
            return redirect('login_user')


    else:
        return render(request,'login_user.html',{})
    
def logout_user(request):
    logout(request)
    messages.success(request,("You were logged Out!"))
    return redirect('home')
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,'Registration Successfull')
            return redirect("home") 
    else:
        form = RegisterUserForm()
    return render(request,'register_user.html',{'form':form})
