from django.urls import path
from seller.views import *
from customer.views import *

urlpatterns = [
    path('exmaple/',example,name="exmaple"),
    path("seller_dash_board/",seller_dashboard_view,name="seller_dash_board"),
    path("seller_changepassword/",password_change_view, name="password_change")
    
]

