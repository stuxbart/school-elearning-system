from django.shortcuts import redirect


class IsTeacherMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_teacher:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('/')
