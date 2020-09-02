from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, generics

from ..serializers import (
    SnippetCourseSerializer,
    CourseSerializer,
    CategorySerializer,
    DetailCategorySerializer,
    CreateCourseSerializer,
    EnrollCourseSerializer,
    ModuleSerializer,
    CreateModuleSerializer,
    SnippetModuleSerializer
)
from ..models import Course, Category, Membership, Module

from accounts.permissions import (
    IsAdminStaffOrReadOnly,
    IsAdminStaffTeacherOrReadOnly,
    IsAdminStaffOwnerOrReadOnly
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.get_used_categories()
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdminStaffOrReadOnly
    ]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action in ['list', 'subcategories', 'tree']:
            return CategorySerializer
        return DetailCategorySerializer

    @action(detail=True)
    def subcategories(self, request, *args, **kwargs):
        category = self.get_object()
        subcategories = category.get_child_categories()

        serializer = self.get_serializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True)
    def tree(self, request, *args, **kwargs):
        category = self.get_object()
        subcategories = category.get_category_tree()

        serializer = self.get_serializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdminStaffTeacherOrReadOnly
    ]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method == "GET":
            return SnippetCourseSerializer
        return CreateCourseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdminStaffOwnerOrReadOnly
    ]
    lookup_field = 'slug'
    serializer_class = CourseSerializer

    # def get_serializer_class(self):
    #     if self.request.method == "GET":
    #         return CourseSerializer
    #     return CreateCourseSerializer


class CourseEnrolAPIView(generics.GenericAPIView):
    serializer_class = EnrollCourseSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self):
        slug = self.kwargs['slug'] or None
        if slug is not None:
            course = get_object_or_404(Course, slug=slug)
            return course
        raise Http404()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_access_key = serializer.validated_data['access_key']
        user = request.user
        course = self.get_object()
        if course.access_key == course_access_key:
            m = Membership(
                user=user,
                course=course,
                method="key"
            )
            m.save()
            return Response({'enrolled': True}, status=status.HTTP_200_OK)
        return Response({'enrolled': False}, status=status.HTTP_400_BAD_REQUEST)


# class ModuleListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Module.objects.all()
#     permission_classes = [
#         permissions.IsAuthenticated,
#         IsAdminStaffTeacherOrReadOnly
#     ]
#
#     def get_serializer_class(self):
#         if self.request.method == "GET":
#             return SnippetModuleSerializer
#         return CreateModuleSerializer
#
#
# class ModuleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Module.objects.all()
#     permission_classes = [
#         permissions.IsAuthenticated,
#         IsAdminStaffOwnerOrReadOnly
#     ]
#     serializer_class = ModuleSerializer


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action in ['list', 'create']:
            permission_classes.append(IsAdminStaffTeacherOrReadOnly)
        else:
            permission_classes.append(IsAdminStaffOwnerOrReadOnly)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return SnippetModuleSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CreateModuleSerializer
        else:
            return ModuleSerializer



# Text / Image / File / Video
# Add content Text / Image / File / Video
# Edit content
# Delete content
# Show / Hide content
# Content Order change
# Create Module
# Edit Module
# Delete Module
# Show/hide module
# Module Order change
