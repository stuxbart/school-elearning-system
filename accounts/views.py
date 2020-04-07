from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        response_obj = {
                'message': 'Pomyślnie zalogowano',
                'username': user.username,
            }
        if user.first_name and user.last_name:
            response_obj['full_name'] = user.first_name + " " + user.last_name
        return JsonResponse(response_obj, status=200)
    return JsonResponse({'message': 'Złe dane logowania'}, status=400)

def logout_view(request):
    logout(request)
    return redirect('home')