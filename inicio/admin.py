from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)

# Mezclar Información del Perfil y del Usuario
class ProfileInline(admin.StackedInline):
    model = Profile

# Extender el Modelo de Usuario
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]
    
# Darse de baja a la antigua usanza
admin.site.unregister(User)

# Vuelva a registrarse de la nueva manera
admin.site.register(User, UserAdmin)
    