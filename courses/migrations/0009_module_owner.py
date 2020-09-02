# Generated by Django 3.1 on 2020-09-02 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def set_module_owner(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Module = apps.get_model('courses', 'Module')
    User = apps.get_model('accounts', 'User')
    default_user = User.objects.get(email='admin@admin.com')
    for module in Module.objects.all():
        if module.owner is not None:
            module.owner = module.course.owner
        else:
            module.owner = default_user
        module.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0008_auto_20200828_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(set_module_owner),
        migrations.AlterField(
            model_name='module',
            name='owner',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.CASCADE,
                                    to=settings.AUTH_USER_MODEL),
        )
    ]
