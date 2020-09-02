from django.http import Http404

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
    CreateCourseSerializer
)
from ..models import Course, Category

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


# enroll_course
# Text / Image / File / Video
# Course by category
# Manage Course List
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
