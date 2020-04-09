from django.contrib import admin

from .models import Subject, Module, Content, Text, Image, File, Video
# Register your models here.

class TextInline(admin.StackedInline):
    model = Text

class ImageInline(admin.StackedInline):
    model = Image

class FileInline(admin.StackedInline):
    model = File

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    model = Content
    list_display = ['module', 'content_type', 'object_id', 'item']   
    inlines = [] 

class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title','subject','description']
    sortable_by = ['subject']
    inlines = []
    

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = [
            "title",
            "slug",     
            "owner",
            "overview",
            "updated",
            "created",
            ]
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
