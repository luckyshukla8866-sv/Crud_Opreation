from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

class StudentPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param="page size"
    max_page_size=10


class EmployeePagination(LimitOffsetPagination):
    default_limit = 3
    max_limit=10    

class EmployeeCursorPagination(CursorPagination):
    page_size=3
    ordering='-emp_id'