from django.contrib import admin

from .models import Subject, Module
# Register your models here.
class ModuleInline(admin.StackedInline):
    model = Module


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

