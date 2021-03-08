from django.contrib import admin

from .models import Course, Module, Content, Text, Image, File, Video, Category, CourseAdmin

admin.site.register(CourseAdmin)
admin.site.register(Text)
admin.site.register(Image)
admin.site.register(File)
admin.site.register(Video)

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
    list_display = ['pk', 'title', 'course', 'description']
    sortable_by = ['course']
    inlines = []


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category']
    prepopulated_fields = {'slug': ('name',)}
