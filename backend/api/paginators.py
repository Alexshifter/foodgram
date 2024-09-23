from rest_framework.pagination import PageNumberPagination

DEFAULT_PAGE_SIZE = 4


class FoodgramPaginator(PageNumberPagination):

    """Стандартная пагинация проекта."""

    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'limit'