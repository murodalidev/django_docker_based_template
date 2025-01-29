from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response

from apps.utils.pagination import CustomPageNumberPagination


class CacheGenericListMixin:
    """
        Inheriting from GenericView is required
    """
    pass
    # cache_timeout = 30*60
    # cache_basename = None
    #
    # def get_queryset(self, *args, **kwargs):
    #     cached_response = cache.get(f"{self.cache_basename}_list")
    #     if cached_response:
    #         return cached_response
    #
    #     # Get data from DB if not cached
    #     response = super().get_queryset(*args, **kwargs)
    #
    #     # Cache the response
    #     cache.set(self.cache_basename, response, timeout=self.cache_timeout)
    #     return response


class CacheGenericRetrieveMixin:
    """
        Inheriting from GenericView is required
    """
    pass
    # cache_timeout = 60*60*24
    # cache_basename = None
    #
    # def retrieve(self, request, *args, **kwargs):
    #     # Generate a cache key for the retrieve view
    #     instance = self.get_object()
    #     lang = request.META.get('HTTP_ACCEPT_LANGUAGE', 'uz')
    #     cache_key = f'{self.cache_basename}_detail_{instance.id}_{lang}'
    #     cached_response = cache.get(cache_key)
    #
    #     if cached_response:
    #         return Response(cached_response)
    #
    #     # Get data from DB if not cached
    #     response = super().retrieve(request, *args, **kwargs)
    #
    #     # Cache the response
    #     cache.set(cache_key, response.data, timeout=self.cache_timeout)
    #     return Response(response.data)


class CreateMixin:

    def create(self, request, *args, **kwargs):
        created_obj = super().create(request, *args, **kwargs)
        obj = get_object_or_404(self.model, id=created_obj.data.get('id'))
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateMixin:

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        obj = self.get_object()
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DestroyMixin:

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_deleted = True
        if hasattr(obj, 'order'):
            obj.order = None
        obj.save()
        data = {
            "success": True,
            "detail": _("Object deleted")
        }
        return Response(data, status=status.HTTP_200_OK)


class CommonMixin(CreateMixin, UpdateMixin, DestroyMixin):
    # pagination_class = CustomPageNumberPagination
    model = None
    serializer_post_class = None

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            assert self.serializer_post_class is not None, (
                    "'%s' should either include a `serializer_class` attribute, "
                    "or override the `get_serializer_class()` method."
                    % self.__class__.__name__
            )
            return self.serializer_post_class

        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.serializer_class


class MultiLanguageRetrieveMixin:
    model = None

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        slug = self.kwargs.get('slug')

        try:
            obj = queryset.get(slug=slug)
        except self.model.DoesNotExist:
            try:
                obj = queryset.get(slug_uz=slug)
            except self.model.DoesNotExist:
                try:
                    obj = queryset.get(slug_ru=slug)
                except self.model.DoesNotExist:
                    obj = queryset.get(slug_en=slug)

        # if accept_language == 'uz':
        #     obj = get_object_or_404(queryset, slug_uz=slug)
        # elif accept_language == 'ru':
        #     obj = get_object_or_404(queryset, slug_ru=slug)
        # elif accept_language == 'en':
        #     obj = get_object_or_404(queryset, slug_en=slug)
        # else:
        #     return Response({"success": False, "detail": _("Invalid accept_language")}, 400)

        self.check_object_permissions(self.request, obj)
        return obj
