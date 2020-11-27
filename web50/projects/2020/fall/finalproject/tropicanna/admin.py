from django.contrib import admin

# Register your models here.
from .models import Customer, Category, Flavor, Product


admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Flavor)
admin.site.register(Product)
