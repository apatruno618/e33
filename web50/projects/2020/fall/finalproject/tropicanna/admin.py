from django.contrib import admin

# Register your models here.
from .models import Customer, Category, Flavor, User, Order, OrderedItem


admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Flavor)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(OrderedItem)
