from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

class StudentPagination(LimitOffsetPagination):
     default_limit = 3
     max_limit=10   

