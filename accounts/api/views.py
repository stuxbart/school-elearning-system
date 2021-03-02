from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from knox.models import AuthToken

from ..models import User
from ..serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    SnippetUserSerializer
)
from ..permissions import (
    IsAdminStaffCurrentUserOrReadOnly,
    IsAdminStaffDeleteOnly
)

from ..documents import UserDocument


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        instance, token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        }, *args, **kwargs)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        instance, token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        }, *args, **kwargs)


class LoggedInUserRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        request = self.request
        valid_args = ['id', 'user_index', 'full_name', 'email',
                      "is_teacher", 'is_staff', 'is_admin']  # ['with_inactive', 'type']
        get_args = request.GET

        if 'with_inactive' in get_args:
            arg = get_args['with_inactive']
            if arg == 1 or 'true':
                users = User.objects.all()
            else:
                users = User.objects.active()
        else:
            users = User.objects.active()

        for arg in get_args:
            if arg in valid_args:
                arg_value = get_args[arg]
                if arg_value:
                    arg_value = arg_value.split(',')
                    if isinstance(arg_value, list) or isinstance(arg_value, tuple):
                        arg_name = f"{arg}__in"
                    else:
                        arg_name = arg
                    users = users.filter(**{arg_name: arg_value})
        return users

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        get_args = request.GET

        if 'type' in get_args:
            valid_types = ['snippet', 'full']
            t = get_args['type']
            if t == valid_types[0]:
                serializer = SnippetUserSerializer(qs, many=True, context={'request': request})
            elif t == valid_types[1]:
                serializer = UserSerializer(qs, many=True, context={'request': request})
            else:
                serializer = SnippetUserSerializer(qs, many=True, context={'request': request})
        else:
            serializer = SnippetUserSerializer(qs, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK, *args, **kwargs)


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdminStaffCurrentUserOrReadOnly,
        IsAdminStaffDeleteOnly,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        with_inactive = self.request.GET.get('with_inactive') or None
        pk = self.kwargs.get('pk')

        if with_inactive is not None:
            obj = get_object_or_404(User.objects.all(), pk=pk)
        else:
            obj = User.objects.active().get(pk=pk)

        self.check_object_permissions(self.request, obj)

        return obj


class UserSearchAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = User.objects.all()
        q = self.request.GET.get('q', None)
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

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        get_args = request.GET

        if 'type' in get_args:
            valid_types = ['snippet', 'full']
            t = get_args['type']
            if t == valid_types[0]:
                serializer = SnippetUserSerializer(qs, many=True, context={'request': request})
            elif t == valid_types[1]:
                serializer = UserSerializer(qs, many=True, context={'request': request})
            else:
                serializer = SnippetUserSerializer(qs, many=True, context={'request': request})
        else:
            serializer = SnippetUserSerializer(qs, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK, *args, **kwargs)