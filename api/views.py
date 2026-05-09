from django.shortcuts import render
from rest_framework.response import Response
from .models import Student, Course, Employee, Salarylog
from .serializers import StudentSerializer,CourseSerializer,EmployeeSerializer, SalarylogSerializer
from rest_framework.decorators import api_view
from django.db import transaction

# Create your views here.
@api_view(['POST'])
def create_employee(request):
    print("hello From outside")
    try:
        name=request.data.get("name")
        salary=request.data.get("salary")
        img=request.FILES.get("img")
        
        if name is None or salary is None:
            return Response({
                    "Status":"Failed",
                    "Data":"Please Provide requierd fileds(name,salary)"
                })
        
        if not isinstance(name,str):
            return Response({
                "Status":"Failed",
                "Data":"Name must be String"
            })
        

        employee=Employee.objects.create(emp_name=name,emp_salary=salary,img=img)

        Salarylog.objects.create(employee=employee,amount=salary)

        return Response({
            "Status":"Sucessfully",
            "Data":"Successfully Employee Created"
        })
    
    except Exception as e :
        return Response({
            "Status" :"Failed",
            "Data": str(e)
        })

@api_view(['GET'])
def fetch_employee(request):
    try:
        data=Employee.objects.all()
        employee=[]
        
        for item in data:
            data_dict={
                "ID":item.emp_id,
                "Name":item.emp_name,
                "Salary":item.emp_salary,
                "Image": request.build_absolute_uri(item.img.url) if item.img else None
            }

            employee.append(data_dict)

        return Response({
            "Status":"Successfully",
            "Data":employee
        })

    except Exception as e:
        return Response({
            "Status":"Failed",
            "Data":str(e)
        })

@api_view(['GET'])
def search_employee(request):
    try:
        id=request.data.get("id")
        name=request.data.get('name')

        if id:
            if id is None:
                return Response({
                    "Status":"Failed",
                    "Data":"Please Provide requierd fileds(id)"
                })
            
            employee=Employee.objects.get(emp_id=id)

            return Response({
                "Status":"Search Sucessfull",
                "Data":{
                    "Id":employee.emp_id,
                    "Name":employee.emp_name,
                    "Salary":employee.emp_salary,
                    "Image": request.build_absolute_uri(employee.img) if employee.img else None
                }
            })
        elif name:
            if name is None:
                return Response({
                    "Status":"Failed",
                    "Data":"Please Provide requierd fileds(id)"
                })
            
            employee=Employee.objects.get(emp_name=name)

            return Response({
                "Status":"Search Sucessfull",
                "Data":{
                    "Id":employee.emp_id,
                    "Name":employee.emp_name,
                    "Salary":employee.emp_salary,
                    "Image": request.build_absolute_uri(employee.img) if employee.img else None
                }
            })

    
    except Exception as e:
        return Response({
            "Status":"Falied",
            "Data":str(e)
        })


@api_view(['PUT','PATCH'])
@transaction.atomic
def update_employee(request):
    try:
        id=request.data.get('id')

        if not id:
            return Response({
                "Status":"Failed",
                "Data":"Please Provide requer field(id)"
            })
        
        employee=Employee.objects.get(emp_id=id)
        employee.emp_name=request.data.get('name')
        employee.emp_salary=request.data.get('salary')
        employee.img=request.FILES.get('img')

        employee.save()

        return Response({
            'Status':"Successfully",
            "Data":"Updated Sucessully"
        })
    
    except Exception as e:
        return Response({
            "Status":"Failed",
            "Data":str(e)
        })



@api_view(['DELETE'])
def delete_employee(request):
    try:
        id = request.data.get('id')
        name=request.data.get('name')

        if id:
            if id is None:
                return Response({
                    "Status":"Failed",
                    "Data":"Please Provide requierd fileds(id)"
                })
            
            employee=Employee.objects.get(emp_id=id)
            employee.delete()

            return Response({
                "Status":"Deleted Sucessfull",
                "Data":{
                    "Id":employee.emp_id,
                    "Name":employee.emp_name,
                    "Salary":employee.emp_salary,
                    "Image": request.build_absolute_uri(employee.img) if employee.img else None
                }
            })
        elif name:
            if name is None:
                return Response({
                    "Status":"Failed",
                    "Data":"Please Provide requierd fileds(id)"
                })
            
            employee=Employee.objects.get(emp_name=name)
            employee.delete()
            return Response({
                "Status":"Deleted Sucessfull",
                "Data":{
                    "Id":employee.emp_id,
                    "Name":employee.emp_name,
                    "Salary":employee.emp_salary,
                    "Image": request.build_absolute_uri(employee.img) if employee.img else None
                }
            })
        
        return Response({
            "Status":"Sucesfully",
            "Data":f"deleted successfully{employee.emp_id}" 
        })
    
    except Exception as e:
        return Response({
            "Status":"Failed",
            "Data":str(e)
        })

        
@api_view(['POST'])
def create_course(request):
    try:
        course_name=request.data.get("course_name")
        student_id=request.data.get("student_id")

        if course_name is None or student_id is None:
            return Response({
                "Status":"Failed",
                "Data":"Please provide the course name and student id"
            })
        
        if not isinstance(course_name,str):
            return Response({
                "Status":"Failed",
                "Data":"Couese name must be String"
            })
               
        student=Student.objects.get(id=student_id)
        course=Course.objects.create(course_name=course_name,student=student)

        return Response({
            "Status" : "Successfully",
            "Data": {
                "Course_name":course.course_name,
                "Student":student.name
            }
        })

    except Student.DoesNotExist as e:
        return Response({
            "Status":"Failed",
            "Data":str(e)
        })

@api_view(['GET'])
def get_course(request):
    try:

        courses=Course.objects.all()
        serializer=CourseSerializer(courses,many=True)

        return Response({
            "Status":"Successfully",
            "Data":serializer.data
        })
    
    except Exception as e:
        return Response({
            "Status":"Failed",
            "Data":str(e)
        })

@api_view(['GET'])
def fetch_all(rerquest):
    try:
        students=Student.objects.all()
        courses=Course.objects.all()
        student_serializer=StudentSerializer(students,many=True)
        course_serializer=CourseSerializer(courses,many=True)

        return Response({
            "Status":"Successfully",
            "Students":student_serializer.data,
            "courses":course_serializer.data
        })
    
    except Exception as e:
        return Response({
            "Status":"Failed",
            "Data":str(e)
        })
    


@api_view(['PUT', 'PATCH'])
def update_course(request):
    try:
        id = request.data.get("course_id")
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
def delete_course(request):
    try:
        id=request.data.get('course_id')
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
def update_student(request):
    try:
        id=request.data.get("id")
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
def delete_student(request):
    try:
        id=request.data.get('id')
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



