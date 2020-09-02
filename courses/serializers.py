from rest_framework import serializers
from .models import Course, Category, Module, Text, Content, Image, Video, File
from accounts.serializers import SnippetUserSerializer


class SnippetModuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Module
        fields = ['url', 'id', 'title', 'description']


class SnippetCourseSerializer(serializers.HyperlinkedModelSerializer):
    owner = SnippetUserSerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ['url', 'id', 'title', 'slug', 'owner', 'overview']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
        }


class ModuleSerializer(serializers.HyperlinkedModelSerializer):
    course = SnippetCourseSerializer(many=False, read_only=True)

    class Meta:
        model = Module
        fields = ['url', 'id', 'title', 'description', 'course', 'order', 'visible']


class CreateModuleSerializer(serializers.HyperlinkedModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Module
        fields = ['title', 'description', 'course', 'visible']
        extra_kwargs = {
            'course': {'required': True},
        }

    def create(self, validated_data):
        owner = validated_data.get('owner')
        course = validated_data['course']
        if owner != course.owner:
            raise serializers.ValidationError("Owners doesn't match")

        return super().create(validated_data)


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    module_set = SnippetModuleSerializer(many=True, read_only=True)
    owner = SnippetUserSerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ['url', 'id', 'title', 'slug', 'owner', 'overview', 'updated', 'created', 'category', 'module_set']
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
        fields = ['url', 'id', 'name', 'slug', 'parent_category']
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


class EnrollCourseSerializer(serializers.Serializer):
    access_key = serializers.CharField()


class BaseContentSerializer(serializers.ModelSerializer):
    owner = SnippetUserSerializer(many=False, read_only=True)
    course = SnippetCourseSerializer(many=False, read_only=True)

    class Meta:
        model = Content
        fields = ['id', 'title', 'owner', 'course', 'module',
                  'visible', 'order', 'item', 'created', 'updated']

    def create(self, validated_data):
        owner = validated_data.get('owner')
        del validated_data['owner']
        module = validated_data['module']

        if owner != module.owner:
            raise serializers.ValidationError("Owners doesn't match")

        if hasattr(self, 'item_class'):
            ItemClass = getattr(self, 'item_class')
            item = ItemClass(**validated_data.get('item'), owner=owner)
            item.save()
            validated_data['item'] = item
        else:
            raise serializers.ValidationError()

        return super().create(validated_data)


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['title', 'content']


class TextContentSerializer(BaseContentSerializer):
    item = TextSerializer(many=False)
    item_class = Text


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['file']


class ImageContentSerializer(BaseContentSerializer):
    item = ImageSerializer(many=False, read_only=True)
    item_class = Image


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['file']


class VideoContentSerializer(BaseContentSerializer):
    item = VideoSerializer(many=False, read_only=True)
    item_class = Video


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file']


class FileContentSerializer(BaseContentSerializer):
    item = FileSerializer(many=False, read_only=True)
    item_class = File
