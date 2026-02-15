from django.shortcuts import render

# Create your views here.
def home(req):
    context = {

    }
    return render(req,"core/home.html",context)
