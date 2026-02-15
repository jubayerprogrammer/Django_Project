from django.urls import path
from customer.views import*


urlpatterns = [
    
    path('dashboard/', dash_bord, name="customer_dashboard"),
    path("password-change/",password_change_view, name="password_change"),

]
