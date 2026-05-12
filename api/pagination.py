from rest_framework.pagination import PageNumberPagination

class StudentPagination(PageNumberPagination):

    page_size = 3

class EmployeePagination(PageNumberPagination):

    page_size = 3