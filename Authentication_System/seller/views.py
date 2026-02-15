from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.decorators import login_and_role_required
from customer.views import *

# Create your views here.
@login_and_role_required("seller")
def example(request):
    return render(request,'seller/exmaple.com')

@login_and_role_required("seller")
def seller_dashboard_view(request):
    return render(request,"seller/dashboard_seller.html")
