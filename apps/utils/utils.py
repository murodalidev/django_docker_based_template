import random
import string
from django.utils.text import slugify


def code_generator(size=5, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



def make_unique_slug(instance, title: str, slug_field: str = 'slug'):
    """
    Django creates unique slugs for model objects.

    :param instance: The model object itself
    :param title: The source text for the slug
    :param slug_field: The field in the model where the slug is stored (default: 'slug')
    :return: A unique slug value
    """
    Klass = instance.__class__
    slug = slugify(title)
    original_slug = slug

    queryset = Klass.objects.filter(**{f"{slug_field}__startswith": slug}).exclude(pk=instance.pk)
    similar_slugs = queryset.values_list(slug_field, flat=True)  # Slug maydonlar ro'yxatini oling

    counter = 1
    while slug in similar_slugs:
        slug = f"{original_slug}-{counter}"
        counter += 1

    return slug