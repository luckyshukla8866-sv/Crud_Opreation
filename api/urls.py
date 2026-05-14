
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
]
