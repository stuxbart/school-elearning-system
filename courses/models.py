from django.db import models
from django.conf import settings 
from django.db.models.signals import pre_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
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
    admins = models.ManyToManyField(
        User, 
        related_name='admin_courses', 
        blank=True,
        through="courses.CourseAdmin"
    )
    overview = models.TextField()
    access_key = models.CharField(max_length=100, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, blank=True, null=True)

    participants = models.ManyToManyField(
        User, 
        related_name='courses', 
        blank=True,
        through="courses.Membership"
    )

    objects = CourseManager()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:details", kwargs={"slug": self.slug})

    def get_category_tree(self):
        if self.category is not None:
            return self.category.get_category_tree()
        else:
            return []


def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance)


pre_save.connect(course_pre_save_receiver, sender=Course)


class CategoryQuerySet(models.query.QuerySet):
    def get_root_categories(self):
        return self.filter(parent_category=None)

    def get_used_categories(self):
        return self.exclude(
            Q(child_categories=None) & Q(course=None)
        )


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(model=self.model, using=self._db)

    def get_root_categories(self):
        return self.get_queryset().get_root_categories()

    def get_used_categories(self):
        return self.get_queryset().get_used_categories()


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

    objects = CategoryManager()

    class Meta:
        ordering = ['name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("courses:category", kwargs={"slug": self.slug})

    def get_category_tree(self):
        categories = []

        def parse(category):
            categories.append(category)
            if category.parent_category:
                parse(category.parent_category)

        parse(self)
        return categories[::-1]

    def get_child_categories(self):
        categories = []

        def parse(category):
            categories.append(category)
            for child_category in category.child_categories.all():
                if child_category not in categories:
                    parse(child_category)

        parse(self)
        return categories


def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance)


pre_save.connect(category_pre_save_receiver, sender=Category)


class ModuleManager(models.Manager):
    def visible(self):
        return self.get_queryset().filter(visible=True)


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    visible = models.BooleanField(default=False, blank=False, null=False)
    order = OrderField(for_fields=['course'], blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ModuleManager()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def move(self, n):
        if isinstance(n, int):
            qs = self.course.module_set
            current_n = self.order
            to_swap = qs.filter(order=n)

            if to_swap.exists():
                to_swap = to_swap.first()
                to_swap.order = current_n
                self.order = n

                to_swap.save()
                self.save()
            else:
                self.order = n
                self.save()
        else:
            self.order = 1
            self.save()
        return self.order

    def move_up(self):
        if self.order != 1:
            return self.move(self.order-1)

    def move_down(self):
        course = self.course
        if self.order != course.module_set.latest('order').order:
            return self.move(self.order+1)


class AvailableContentManager(models.Manager):
    def get_available_queryset(self, user):
        qs = super().get_queryset()
        return qs.filter(module__course__participants__in=[user])


class ContentManager(AvailableContentManager):
    def get_texts(self, user):
        text_type = ContentType.objects.get_for_model(Text)
        return self.get_available_queryset(user).filter(content_type=text_type)

    def get_images(self, user):
        image_type = ContentType.objects.get_for_model(Image)
        return self.get_available_queryset(user).filter(content_type=image_type)

    def get_videos(self, user):
        video_type = ContentType.objects.get_for_model(Video)
        return self.get_available_queryset(user).filter(content_type=video_type)

    def get_files(self, user):
        file_type = ContentType.objects.get_for_model(File)
        return self.get_available_queryset(user).filter(content_type=file_type)


class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    visible = models.BooleanField(default=False, blank=False, null=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(for_fields=['module'], blank=True)

    objects = ContentManager()

    class Meta:
        ordering = ['order']

    @property
    def owner(self):
        if self.item:
            return self.item.owner
        else:
            return None

    @property
    def title(self):
        if self.item:
            return self.item.title
        else:
            return None

    @property
    def course(self):
        return self.module.course

    @property
    def created(self):
        return self.module.created

    @property
    def updated(self):
        return self.module.updated

    def __str__(self):
        return f"{self.order}. {self.item.title}"

    def move(self, n):
        if isinstance(n, int):
            if n > 0:
                qs = self.module.content_set
                current_n = self.order
                to_swap = qs.filter(order=n)

                if to_swap.exists():
                    to_swap = to_swap.first()
                    to_swap.order = current_n
                    self.order = n

                    to_swap.save()
                    self.save()
                else:
                    self.order = n
                    self.save()
            else:
                self.order = 1
                self.save()
        return self.order

    def move_up(self):
        if self.order != 1:
            return self.move(self.order-1)

    def move_down(self):
        module = self.module
        if self.order != module.content_set.latest('order').order:
            return self.move(self.order+1)


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


class CourseAdmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    can_add_participants = models.BooleanField(default=False)
    can_add_content = models.BooleanField(default=False)
    can_remove_participants = models.BooleanField(default=False)
    can_remove_content = models.BooleanField(default=False)
    can_edit_course = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user} admin of {self.course}"