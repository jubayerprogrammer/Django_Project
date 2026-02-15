from django.contrib import admin
from product.models import Product

# Register your models here.
class ProductModelAdmin(admin.ModelAdmin):
    model = Product
    list_display = ["id","name","descriptions","price"]

admin.site.register(Product,ProductModelAdmin)
