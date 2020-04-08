from django.contrib import admin

from .models import Subject, Module, Content
# Register your models here.
class ContentInline(admin.StackedInline):
    model = Content

class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['subject','title','description']
    sortable_by = ['subject']
    inlines = [ContentInline]

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
    inlines = [ModuleInline]
