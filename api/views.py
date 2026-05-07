from django.shortcuts import render
from rest_framework.response import Response
from .models import Student, Course
from .serializers import StudentSerializer,CourseSerializer
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['POST'])
def create_course(request):
    try:
        course_name=request.data.get("course")

        if course_name is None:
            return Response({
                "Status":"Failed",
                "Data":"Please provide the course name"
            })
        Course.objects.create(course_name=course_name)
        return Response({
            "Status" : "Successfully",
            "Data": "Successfully created Course"
        })

    except Course.DoesNOtexoist as e:
        return Response({
            "Status":"Failed",
            "Data":str(e)
        })

@api_view(['GET'])
def get_course(request):
    courses=Course.objects.all()
    serializer=CourseSerializer(courses,many=True)
    
    return Response({
        "Status":"Successfully",
        "Data":serializer.data
    })

@api_view(['GET'])
def fetch_all(rerquest):
    students=Student.objects.all()
    courses=Course.objects.all()
    student_serializer=StudentSerializer(students,many=True)
    course_serializer=CourseSerializer(courses,many=True)
   
    return Response({
        "Status":"Successfully",
        "Students":student_serializer.data,
        "courses":course_serializer.data
    })

@api_view(['PUT', 'PATCH'])
def update_course(request,id):
    try:
        if id is None:
            return Response({
                "Status":"Failed",
                "Data":"Enter a Valid Id"
            })
        course=Course.objects.get(id=id)
        course.course_name=request.data.get('course_name')
        course.save()

        return Response({
            "Status":"Successfully",
            "Data":"Course updated sucessfully"
        })

    except Course.DoesNotExist as e:
        return Response({
            "Status":"Failed",
            "Data":str(e)
        })

@api_view(['DELETE'])
def delete_course(request,id):
    try:
        if id is None:
            return Response({
                "status":"Falied",
                "Data":"Please enter a valid course id"
            })
        course=Course.objects.get(id=id)
        course.delete()
        return Response({
            "Status":"Sucessfully",
            "Data":"Course deleted successfully"
        })
    except Course.DoesNotExist as e:
        return Response({
            "Status":"Failed",
            "Data":str(e)
        })
    
@api_view(['POST'])
def create_students(request):
    try:
        std_name = request.data.get('name')
        std_age=request.data.get('age')
        std_email=request.data.get('email')
        
        if std_name is None or std_age is None or std_email is None:
            return Response({
                "Status" : "Failed",
                "Errors":"Please Provide all requierd fileds(name,age,email)"
            })
        
        Student.objects.create(name=std_name,age=std_age,email=std_email)
        
        return Response({
            "Status": "Successfully",
            "Data": "Successfully created Student"
        })
    
    except Exception as e:
        return Response({
            "Status": "Failed",
            "Errors":str(e)
        })
    

@api_view(['GET'])
def get_students(request):
    try:
        students = Student.objects.all()
        serializer=StudentSerializer(students,many=True)
        return Response({
            "Status" : "Success",
            "Data" : serializer.data
        })
    except Exception as e:
        return Response({
            "Status" : "Failed",
            "Errors" : str(e)
        })

@api_view(['PUT', 'PATCH'])
def update_student(request,id):
    try:
        if id is None:
            return Response({
                "Status" : "Failed",
                "Errors" : "Please provide the student id"
            })
        
        students=Student.objects.get(id=id)
        students.name=request.data.get('name')
        students.age=request.data.get('age')
        students.email=request.data.get('email')
        
        students.save()

        return Response({
            "Status":"Success",
            "Data": "Successfully updates Student"})

    except Student.DoesNotExist:
        return Response({
            "Status" : "Failed",
            "Errors": "Student not found"})
    
    
@api_view(['DELETE'])
def delete_student(request,id):
    try:
        if id is None:
            return Response({
                "Status" : "Failed",
                "Errors" : "Please provide the student id"
            })
        
        students=Student.objects.get(id=id)
        students.delete()
        return Response({
            "Status" : "Success",
            "Errors" : "Successfully deleted Student"
        })
    except Student.DoesNotExist:
        return Response({
            "Status" : "Failed",
            "Errors" : "Student not found"
        })



