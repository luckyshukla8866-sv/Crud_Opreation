
from django.urls import path,include
from .views import *

urlpatterns = [
    path('create-student/', create_students),
    path('fetch-student/', get_students),
    path('delete-student/<int:id>/',delete_student),
    path('update-student/<int:id>/',update_student),
    path('create-course/', create_course),
    path('delete-course/<int:id>/', delete_course),
    path('update-course/<int:id>/', update_course),
    path('fetch-course/',get_course),
    path('fetch-all/',fetch_all),
]
