from django.contrib import admin
from scanner.models import qr_code

# Register your models here.
@admin.register(qr_code)
class ar_admin(admin.ModelAdmin):
    list_display = [field.name for field in qr_code._meta.fields]