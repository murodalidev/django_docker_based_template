from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomPageNumberPagination(LimitOffsetPagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):
        self.request = request  # Store the request for later use
        self.count = self.get_count(queryset)
        self.limit = self.get_page_size(request)
        self.current_page = self.get_page_number(request)
        self.offset = (self.current_page - 1) * self.limit

        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        return list(queryset[self.offset:self.offset + self.limit])

    def get_page_number(self, request):
        try:
            return int(request.query_params.get(self.page_query_param, 1))
        except ValueError:
            return 1

    def get_page_size(self, request):
        try:
            return int(request.query_params.get(self.page_size_query_param, self.default_limit))
        except ValueError:
            return self.default_limit

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.count,
            'page': self.current_page,
            'page_size': self.limit,
            'results': data
        })

    def get_next_link(self):
        if not self.has_next():
            return None
        url = self.request.build_absolute_uri()
        return self._replace_query_param(url, self.page_query_param, self.current_page + 1)

    def get_previous_link(self):
        if not self.has_previous():
            return None
        url = self.request.build_absolute_uri()
        return self._replace_query_param(url, self.page_query_param, self.current_page - 1)

    def has_next(self):
        return self.current_page * self.limit < self.count

    def has_previous(self):
        return self.current_page > 1

    def _replace_query_param(self, url, key, val):
        querystring = self.request.query_params.copy()
        querystring[key] = val
        return f'{url.split("?")[0]}?{querystring.urlencode()}'
