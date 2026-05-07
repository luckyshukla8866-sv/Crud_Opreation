from django.shortcuts import render
from rest_framework.response import Response
from .models import Student, Course
from .serializers import StudentSerializer,CourseSerializer
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['POST'])
def create_course(request):
    serializer = CourseSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "data": serializer.data
        })

    return Response({
        "status": "error",
        "errors": serializer.errors
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
        courese=Course.objects.get(id=id)
    except Course.DoesNotExist as e:
        return Response({
            "Status":"Failed",
            "Data":str(e)
        })
    serializer=CourseSerializer(courese,data=request.data,partial=(request.method=='PATCH'))

    if serializer.is_valid():
        serializer.save()
        return Response({
            "Status" : "Success",
            "Data" : serializer.data
        })
    else:
        return Response({
            "Status" : "Failed",
            "Errors" : serializer.errors
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
            "status": "Success",
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

    except Student.DoesNotExist:
        return Response({
            "Status" : "Failed",
            "Errors": "Student not found"})
    serializer=StudentSerializer(students,data=request.data,partial=(request.method=='PATCH'))

    if serializer.is_valid():
        serializer.save()
        return Response({
            "Status" : "Success",
            "Data" : serializer.data
        })
    else:
        return Response({
            "Status" : "Failed",
            "Errors" : serializer.errors
        })
    
    
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



