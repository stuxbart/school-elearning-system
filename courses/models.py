from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.shortcuts import reverse

from django.db.models import Count, Q

from .utils import slug_generator
from .fields import OrderField

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
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    overview = models.TextField()
    # many owners
    access_key = models.CharField(max_length=100, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = CourseManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("manager:update", kwargs={"slug": self.slug})


def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance)


pre_save.connect(course_pre_save_receiver, sender=Course)


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(max_length=50)
    parent_category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='child_categories',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_category_tree(self):
        categories = []

        def parse(category):
            categories.append(category)
            if category.parent_category:
                parse(category.parent_category)

        parse(self)
        return categories


def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance)


pre_save.connect(course_pre_save_receiver, sender=Category)


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    visible = models.BooleanField(default=False, blank=False, null=False)
    order = OrderField(for_fields=['course'], blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    visible = models.BooleanField(default=False, blank=False, null=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(for_fields=['module'], blank=True)

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

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


join_methods = (
    ('key', 'Key'),
    ('owner', "Added by owner")
)


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=20, choices=join_methods)
