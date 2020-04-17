from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.shortcuts import reverse

from django.db.models import Sum, Count, Q

from .utils import slug_generator

User = settings.AUTH_USER_MODEL

class CourseQuerySet(models.query.QuerySet):
    pass
    # def content_count(self, *args, **kwargs):
    #     obj = self.get(*args, **kwargs)
    #     text_type = ContentType.objects.get_for_model(Text)
    #     image_type = ContentType.objects.get_for_model(Image)
    #     modules = obj.module_set.annotate(
    #             texts=Count('content', filter=Q(content__content_type=text_type))
    #         ).annotate(
    #             images=Count('content', filter=Q(content__content_type=image_type))
    #         )
    #     #obj.annotate(Sum('images'), Sum('texts'))
    #     return modules.aggregate(Sum('images'), Sum('texts'))

    # def objects_with_counts(self):
    #     text_type = ContentType.objects.get_for_model(Text)
    #     image_type = ContentType.objects.get_for_model(Image)
    #     file_type = ContentType.objects.get_for_model(File)
    #     video_type = ContentType.objects.get_for_model(Video)
    #     objects = self.all().annotate(
    #         texts=Count('module__content', filter=Q(module__content__content_type=text_type)),
    #         images=Count('module__content', filter=Q(module__content__content_type=image_type)),
    #         files=Count('module__content', filter=Q(module__content__content_type=file_type)),
    #         videos=Count('module__content', filter=Q(module__content__content_type=video_type)),
    #     )
    #     return objects


class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, self._db)

    def all(self):
        text_type = ContentType.objects.get_for_model(Text)
        image_type = ContentType.objects.get_for_model(Image)
        file_type = ContentType.objects.get_for_model(File)
        video_type = ContentType.objects.get_for_model(Video)
        objects = self.get_queryset().all().annotate(
            texts=Count('module__content', filter=Q(module__content__content_type=text_type)),
            images=Count('module__content', filter=Q(module__content__content_type=image_type)),
            files=Count('module__content', filter=Q(module__content__content_type=file_type)),
            videos=Count('module__content', filter=Q(module__content__content_type=video_type)),
        )
        return objects



class Course(models.Model):
    title       = models.CharField(max_length=255)
    slug        = models.SlugField(unique=True)
    owner       = models.ForeignKey(User, on_delete=models.CASCADE)
    overview    = models.TextField()
    # many owners
    access_key  = models.CharField(max_length=100, blank=True, null=True)
    updated     = models.DateTimeField(auto_now=True)
    created     = models.DateTimeField(auto_now_add=True)

    objects = CourseManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("manager:update", kwargs={"slug": self.slug})
    

def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance)

pre_save.connect(course_pre_save_receiver, sender=Course)

class Module(models.Model):
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    title       = models.CharField(max_length=255)
    description = models.TextField()
    # ordering
    created     = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Content(models.Model):
    module          = models.ForeignKey(Module, on_delete=models.CASCADE)
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    item            = GenericForeignKey('content_type', 'object_id')


class ItemBase(models.Model):
    owner       = models.ForeignKey(User, on_delete=models.CASCADE)
    title       = models.CharField(max_length=255)
    updated     = models.DateTimeField(auto_now=True)
    created     = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(f"courses:{self.__class__.__name__.lower()}_detail", kwargs={"pk": self.pk})
    

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')
    
class Video(ItemBase):
    file = models.URLField()