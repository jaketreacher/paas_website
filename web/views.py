from django.shortcuts import render

def home(request):
    return render(request, "web/pages/home.html")
 
def about(request):
    return render(request, "web/pages/about.html")
