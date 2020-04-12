from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .utils import slug_generator

User = settings.AUTH_USER_MODEL

# Create your models here.
class Course(models.Model):
    title       = models.CharField(max_length=255)
    slug        = models.SlugField(unique=True)
    owner       = models.ForeignKey(User, on_delete=models.CASCADE)
    overview    = models.TextField()
    # many owners
    access_key  = models.CharField(max_length=100, blank=True, null=True)
    updated     = models.DateTimeField(auto_now=True)
    created     = models.DateTimeField(auto_now_add=True)

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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    updated     = models.DateTimeField(auto_now=True)
    created     = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.title

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')
    
class Video(ItemBase):
    file = models.URLField()