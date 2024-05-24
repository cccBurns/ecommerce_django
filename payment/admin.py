from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

# Register the model on the admin section thing
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# Create an orderitem inline
class OrderItemInLine(admin.StackedInline):
    model = OrderItem
    extra = 0
    
# Extend out order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "shipped", "date_shipped"]
    inlines = [OrderItemInLine]
    
# Unregister Order Model
admin.site.unregister(Order)

# Re-Register our Order and orderItems
admin.site.register(Order, OrderAdmin)


