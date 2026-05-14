from django.shortcuts import render
from rest_framework.response import Response
from .models import Student, Course
from .serializers import StudentSerializer,CourseSerializer
from rest_framework.decorators import api_view
from django.db import transaction
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from rest_framework import status
from .pagination import StudentPagination
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.views import APIView

# Create your views here. 
    
@api_view(['POST'])
def create_students(request):
    try:
        std_name = request.data.get('name')
        std_age=request.data.get('age')
        std_email=request.data.get('email')
        
        if std_name is None:
            return Response({
                "status":"failed",
                "message":"please Provide requer field(name)"
            },status=status.HTTP_404_NOT_FOUND)
        
        if std_age is None :
            return Response({
                "status":"failed",
                "message":"please Provide requer field(age)"
            },status=status.HTTP_404_NOT_FOUND)
        
        if std_email is None:
            return Response({
                "status":"failed",
                "message":"please Provide requer field(email)"
            },status=status.HTTP_404_NOT_FOUND)

        
        Student.objects.create(name=std_name,age=std_age,email=std_email)
        
        return Response({
            "status":"sucessfully",
            "message":"created employee detail",
        },status=status.HTTP_201_CREATED)
    
    except Exception as e :
        return Response({
            "status" :"failed",
            "messge": str(e),
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def get_students(request):
    try:
        students = Student.objects.all()

        paginator=StudentPagination()
        paginated_student=paginator.paginate_queryset(students,request)

        serializer=StudentSerializer(paginated_student,many=True)


        return paginator.get_paginated_response({
            "status": "Success",
            "Data": serializer.data
        })
    
    except Exception as e :
        return Response({
            "status" :"failed",
            "messge": str(e),
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT', 'PATCH'])
def update_student(request):
    try:
        id=request.data.get("id")
        if id is None:
            return Response({
                "status":"failed",
                "message":"please Provide requer field(id)"
            },status=status.HTTP_404_NOT_FOUND)
        
        students=Student.objects.get(id=id)
        students.name=request.data.get('name')
        students.age=request.data.get('age')
        students.email=request.data.get('email')
        
        students.save()

        return Response({
            "status":"sucessfully",
            "message":"created employee detail",
        },status=status.HTTP_201_CREATED)

    except Student.DoesNotExist:
        return Response({
            "status":"error",
            "message":"does not exist",
        }, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['DELETE'])
def delete_student(request):
    try:
        id=request.data.get('id')
        if id is None:
            return Response({
                "status":"failed",
                "message":"please Provide requer field(id)"
            },status=status.HTTP_404_NOT_FOUND)
        
        students=Student.objects.get(id=id)
        students.delete()

        return Response({
            "status":"deleted Sucesfully",
            "message":f"remove student",
        },status=status.HTTP_200_OK)
    
    except Student.DoesNotExist:
        return Response({
            "status":"error",
            "message":"does not exist",
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e :
        return Response({
            "status" :"failed",
            "messge": str(e),
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
      
@api_view(['POST'])
def create_course(request):
    try:
        course_name=request.data.get("course_name")
        student_id=request.data.get("student_id")

        if course_name is None:
            return Response({
                "status":"failed",
                "message":"please Provide requer field(name)"
            },status=status.HTTP_404_NOT_FOUND)
        
        if student_id is None:
            return Response({
                "status":"failed",
                "message":"please Provide requer field(id)"
            },status=status.HTTP_404_NOT_FOUND)
        
               
        student=Student.objects.get(id=student_id)
        course=Course.objects.create(course_name=course_name,student=student)

        return Response({
            "status":"sucessfully",
            "message":"created student detail",
        },status=status.HTTP_201_CREATED)

    except Student.DoesNotExist:
        return Response({
            "status":"error",
            "message":"does not exist",
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_course(request):
    try:

        courses=Course.objects.all()
        serializer=CourseSerializer(courses,many=True)

        return Response({
            "status":"successfully",
            "message":"detail of course",
            "data":serializer.data
        },status=status.HTTP_200_OK)
    
    except Exception as e :
        return Response({
            "status" :"failed",
            "messge": str(e),
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

@api_view(['GET'])
def fetch_all(rerquest):
    try:
        students=Student.objects.all()
        courses=Course.objects.all()
        student_serializer=StudentSerializer(students,many=True)
        course_serializer=CourseSerializer(courses,many=True)

        return Response({
            "status":"successfully",
            "students":student_serializer.data,
            "courses":course_serializer.data
        },status=status.HTTP_200_OK)
    
    except Exception as e :
        return Response({
            "status" :"failed",
            "messge": str(e),
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['PUT', 'PATCH'])
def update_course(request):
    try:
        id = request.data.get("course_id")
        if id is None:
            return Response({
                "status":"failed",
                "message":"please Provide requer field(id)"
            },status=status.HTTP_404_NOT_FOUND)
        
        course=Course.objects.get(id=id)
        course.course_name=request.data.get('course_name')
        course.save()

        return Response({
            "status":"success",
            "message":"udate successful",
        }, status=status.HTTP_200_OK)

    except Course.DoesNotExist:
        return Response({
            "status":"error",
            "message":"does not exist",
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_course(request):
    try:
        id=request.data.get('course_id')
        if id is None:
            return Response({
                "status":"failed",
                "message":"please Provide requer field(id)"
            },status=status.HTTP_404_NOT_FOUND)
        
        course=Course.objects.get(id=id)
        course.delete()

        return Response({
            "status":"deleted Sucesfully",
            "message":f"remove student",
        },status=status.HTTP_200_OK)
    
    except Course.DoesNotExist:
        return Response({
            "status":"error",
            "message":"does not exist",
        }, status=status.HTTP_404_NOT_FOUND)



