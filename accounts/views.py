from django.shortcuts import redirect, reverse
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView



from .documents import UserDocument
from .forms import UserChangePhotoForm, UserInfoUpdateForm

from courses.mixins import PathMixin, PathText, PathLink


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


class UserHomeView(PathMixin, LoginRequiredMixin, DetailView):
    template_name = 'accounts/user_home.html'
    model = User

    def get_paths(self):
        return [
            PathText("Home"),
            PathLink("Profile", reverse("accounts:my_profile"))
        ]

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/user_detail.html'
    queryset = User.objects.active()


class UserEditView(PathMixin, LoginRequiredMixin, DetailView):
    template_name = 'accounts/user_edit.html'

    def get_paths(self):
        return [
            PathText("Home"),
            PathLink("Profile", reverse("accounts:my_profile")),
            PathLink("Update", reverse("accounts:my_profile_update"))
        ]
        
    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['forms'] = {
            'photo': {
                'instance': UserChangePhotoForm(),
                'action': reverse("accounts:my_profile_update_photo")
            },
            'password': {
                'instance': PasswordChangeForm(user),
                'action': reverse("accounts:password_change")
            },
            'info': {
                'instance': UserInfoUpdateForm(initial={"info": user.info}),
                'action': reverse("accounts:my_profile_update_info")
            }
        }
        return context


class UserPhotoUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserChangePhotoForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse("accounts:my_profile_update")
        

class UserInfoUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserInfoUpdateForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse("accounts:my_profile_update")


class UserPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse("accounts:my_profile_update")



class UserSearchListView(LoginRequiredMixin, ListView):
    template_name = 'accounts/user_list.html' # todo

    def get_queryset(self):
        qs = User.objects.all()
        q = self.request.GET.get('q')
        if q:
            q = q.lower()
            if q.isdecimal():
                should = [
                    {
                        "term": {
                            "user_index": q
                        }
                    }
                ]
            else:
                should = [
                    {
                        "fuzzy": {
                            "full_name": {
                                "value": q,
                                "fuzziness": "AUTO",
                                "prefix_length": 3,
                                "transpositions": True,
                            }
                        }
                    },
                    {
                        "prefix": {
                            "full_name": q
                        }
                    }
                    
                ]
            s = UserDocument.search().query("bool", should=should)

            qs = s.to_queryset()
        else:
            qs = User.objects.none()
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q', None)
        return context