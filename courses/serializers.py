from rest_framework import serializers
from .models import Course, Category, Module
from accounts.serializers import SnippetUserSerializer


class SnippetModuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Module
        fields = ['url', 'title', 'description']


class SnippetCourseSerializer(serializers.HyperlinkedModelSerializer):
    owner = SnippetUserSerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ['url', 'title', 'slug' ,'owner', 'overview']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
        }


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    module_set = SnippetModuleSerializer(many=True, read_only=True)
    owner = SnippetUserSerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ['url', 'title', 'slug', 'owner', 'overview', 'updated', 'created', 'category', 'module_set']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'category': {'lookup_field': 'slug'},
        }


class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'overview', 'category']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['url', 'name', 'slug', 'parent_category']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'parent_category': {'lookup_field': 'slug'}
        }


class DetailCategorySerializer(serializers.HyperlinkedModelSerializer):
    course_set = SnippetCourseSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['url', 'name', 'slug', 'parent_category', 'course_set']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'parent_category': {'lookup_field': 'slug'}
        }
