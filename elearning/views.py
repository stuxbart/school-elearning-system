from django.shortcuts import render, redirect

def home_view(request):
    print(request.user.courses.all())
    return render(request, 'home/home.html', {})
