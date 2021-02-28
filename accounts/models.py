from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

from courses.utils import user_index_generator
# from courses.models import Course


class UserQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class UserManager(BaseUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def create_user(self,
                    email,
                    full_name=None,
                    password=None,
                    is_active=True,
                    is_staff=False,
                    is_teacher=False,
                    is_admin=False):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have password")
        user_obj = self.model(
            email=email,
            full_name=full_name,
        )

        user_obj.user_index = user_index_generator(user_obj)
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.teacher = is_teacher
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_teacher(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_teacher=True,
        )
        return user

    def create_staffuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user

    def active(self):
        return self.get_queryset().active()


class User(AbstractBaseUser):
    user_index = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    teacher = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)  # superuser
    timestamp = models.DateTimeField(auto_now_add=True)

    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='user_images', null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    # department = models.CharField(max_length=200, null=True, blank=True)
    # class
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.user_index:
            return self.user_index
        else:
            return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.user_index

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_teacher(self):
        return self.teacher

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


from django.db.models.signals import pre_save


def pre_save_user_receiver(sender, instance, *args, **kwargs):
    if not instance.user_index:
        instance.user_index = user_index_generator(instance)


pre_save.connect(pre_save_user_receiver, sender=User)
