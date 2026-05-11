
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

#router = DefaultRouter()
#router.register(r'images', Employee, basename='image')

urlpatterns = [
    path('create-student/', create_students),
    path('fetch-student/', get_students),
    path('delete-student/',delete_student),
    path('update-student/',update_student),
    path('create-course/', create_course),
    path('delete-course/', delete_course),
    path('update-course/', update_course),
    path('fetch-course/',get_course),
    path('fetch-all/',fetch_all),
    path('fetch-employee/',fetch_employee),
    path('create-employee/',create_employee),
    path('delete-employee/',delete_employee),
    path('update-employee/',update_employee),
    path('search_employee/',search_employee),

]

