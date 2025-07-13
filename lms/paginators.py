from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom pagination class that sets the default page size and maximum page size.
    """
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10
