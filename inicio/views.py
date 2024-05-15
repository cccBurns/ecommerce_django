from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Usuario y Contraseña Correcta"))
            return redirect('home')   
        else:
            messages.success(request, ("Contraseña Incorrecta"))
            return redirect('login')
    else:        
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Su cuenta se encuentra cerrada."))
    return redirect('home')

def register_user(request):
    
     return render(request, 'register.html', {})