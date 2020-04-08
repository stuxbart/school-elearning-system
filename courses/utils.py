import random
import string
from django.utils.text import slugify

def random_string_generator(length=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))

def slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug)
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(slug=slug, randstr=random_string_generator(length=5))
        return slug_generator(instance, new_slug=new_slug)
    return slug

def user_index_generator(instance):
    index = random_string_generator(length=6, chars=string.digits)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(user_index=index)
    if qs_exists:
        return user_index_generator(instance)
    return index