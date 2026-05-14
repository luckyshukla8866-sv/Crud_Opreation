
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

#router = DefaultRouter()
#router.register(r'images', Employee, basename='image')

urlpatterns = [
    path('fetch-employee/',fetch_employee),
    path('fetch-cursor-employee/',fetch_cursor_employee),
    path('create-employee/',create_employee),
    path('delete-employee/',delete_employee),
    path('update-employee/',update_employee),
    path('search-employee/',search_employee),       

]

