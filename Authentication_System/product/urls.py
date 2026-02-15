from django.urls import path
from product.views import *
urlpatterns = [
    path("list/",product_list,name="product_list"),
    path("<int:pk>/",product_details,name="product_detail"),
    path("add/",product_add,name="product_add"),
    path("<int:pk>/delete/",product_delete,name="product_delete"),
    path("<int:pk>/edit/",product_edit,name="product_edit")
    
]

