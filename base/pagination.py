from rest_framework.pagination import PageNumberPagination


class DefaultProjectPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'