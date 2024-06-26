from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

def search(request):
    # Determinar si llenaron el Form
    if request.method == "POST":
        # Obtencion del termino de busqueda
        searched = request.POST['searched']
        # Consulta a la base de datos (La funcion 'Q' realiza consultas con condiciones OR)  
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        # Test for null
        if not searched:
            messages.success(request, "Producto no encontrado")
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {'searched':searched})
    else:
        return render(request, "search.html", {})
    


def update_info(request):
    if request.user.is_authenticated:
        # Obtener Usuario
        current_user = Profile.objects.get(user__id=request.user.id)
        # Obtener Direccion de envio del usuario
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Creacion de instancias de formularios
        # Get original user form
        form = UserInfoForm(request.POST or None, instance=current_user)
        # Get Users Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        # Validacion y guardado de formularios
        if form.is_valid() or shipping_form.is_valid():
            # Save original form
            form.save()
            # Save shipping form
            shipping_form.save()
            
            messages.success(request, "Informacion Actualizada!")
            return redirect('home')
        return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form })
    else:
        messages.success(request, "Debes loguearte para tener acceso a esta pagina")
        return redirect('home')   

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Tu Contraseña ah sigo Cambiada Correctamente")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
            
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form':form})
    else:
        messages.success(request, "Debes loguearte para ver esta pagina")
        return redirect('home')
    
    return render(request, "update_password.html", {})
    

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
            
            login(request, current_user)
            messages.success(request, "Perfil Actualizado!")
            return redirect('home')
        return render(request, "update_user.html", {'user_form':user_form})
    else:
        messages.success(request, "Debes loguearte para tener acceso a esta pagina")
        return redirect('home')   

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories":categories})
    

def category(request, foo):
    # Reemplazo Guiones por Espacios
    foo = foo.replace('-', '')
    # Toma la Categoria de la URL
    # Intenta Buscar la Categoria en la Base de Datos
    try:
        # Busqueda de Categoria
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})

    except:
        messages.success(request, ("Esa categoria no existe"))
        return redirect('home')
    
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def contacto(request):
    return render(request, 'contacto.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Hacer Algunas Cosas del Carrito de Compras
            current_user = Profile.objects.get(user__id=request.user.id)
            # Obtener su Carrito Guardado de la base de Datos
            saved_cart = current_user.old_cart
            # Convertir String de BD a Diccionario
            if saved_cart:
                # Convertir a Diccionario usando JSON
                converted_cart = json.loads(saved_cart)
                # Añadir el diccionario del carrito cargado a nuestra sesión
                # Obtener el Carrito
                cart = Cart(request)
                # Loop thru the cart and add the items from the database
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            
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
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Cuenta Creada Exitosamente"))
            return redirect('update_user')
        else:
            messages.success(request, ("Oops!, Intentalo Nuevamente"))
            return redirect('register')
            
    else:            
        return render(request, 'register.html', {'form':form})