from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import permission_required
from product.models import Product
from product.forms import ProductForm
from django.contrib import messages
from account.decorators import login_and_role_required,login_required

# Create your views here.
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request,"product/product_list.html",{"object":products})
@login_required
def product_details(request,pk):
    product = get_object_or_404(Product,pk=pk)
    return render(request,"product/detail.html",{"product": product})

@login_required
@permission_required("product.add_product",raise_exception=True)
def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"The product add successfull")
            
            return redirect("product_add")
    else:
        form = ProductForm()
    return render(request,"product/add.html",{"form":form})

@login_required
@permission_required("product.delete_product",raise_exception=True)
def product_delete(request,pk):
    product = get_object_or_404(Product,pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request,"The product delete succesful")
        return redirect("product_list")
    return render(request,"product/delete.html",{"product":product})

@login_required
@permission_required("product.change_product",raise_exception=True)
def product_edit(request,pk):
    product = get_object_or_404(Product,pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance= product)
    return render(request,"product/add.html",{"form":form})

        


   








