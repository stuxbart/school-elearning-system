from django.shortcuts import render, redirect
from information.models import News


def home_view(request):
    news = News.objects.all()[:6]
    return render(request, 'home/home.html', {"news": news})
