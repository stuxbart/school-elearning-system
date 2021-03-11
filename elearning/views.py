from django.shortcuts import render, redirect
from information.models import News
from django.core.cache import caches
from django.views.decorators.cache import cache_page


@cache_page(caches['default'].default_timeout)
def home_view(request):
    news = News.objects.all()[:6]
    return render(request, 'home/home.html', {"news": news})
