from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Subject(models.Model):
    title       = models.CharField(max_length=255)
    slug        = models.SlugField(unique=True)
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    overview    = models.TextField()
    # enrolled
    # many owners
    updated     = models.DateTimeField(auto_now=True)
    created     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Module(models.Model):
    subject     = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title       = models.CharField(max_length=255)
    description = models.TextField()
    # ordering
    created     = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    