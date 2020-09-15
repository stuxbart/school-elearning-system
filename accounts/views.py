from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.generic import DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model


User = get_user_model()


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        if len(username) == 6 and username.isdigit():
            qs = User.objects.filter(user_index=username)
            if qs is not None:
                user_obj = qs.first()
                email = user_obj.email
            else:
                email = username
        else:
            email = username
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            response_obj = {
                'message': 'Successfully logged in',
                'username': user.email,
                'teacher': user.is_teacher,
            }
            if user.full_name:
                response_obj['full_name'] = user.full_name
            return JsonResponse(response_obj, status=200)
        return JsonResponse({'message': 'Bad authentication credentials'}, status=400)
    else:
        return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('home')


class UserHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/user_home.html'
    model = User

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/user_detail.html'
    queryset = User.objects.active()
