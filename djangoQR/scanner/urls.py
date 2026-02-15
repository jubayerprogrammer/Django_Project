from django.urls import path
from scanner.views import generate_qr,scan_qr

urlpatterns = [
    path("generate_qr/",generate_qr,name="generate_qr"),
    path("scan_qr",scan_qr,name="scan_qr"),
    
]
