from rest_framework.pagination import PageNumberPagination

from foodgram_backend.constants import DEFAULT_PAGE_SIZE


class FoodgramPaginator(PageNumberPagination):

    """Стандартная пагинация проекта."""

    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'limit'
