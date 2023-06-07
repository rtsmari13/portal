from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)

class UserLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10
    
class UserPageNumberPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param ='count'
    max_page_size = 2