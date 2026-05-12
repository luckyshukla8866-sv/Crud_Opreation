from django.shortcuts import render
from rest_framework.response import Response
from .models import Student, Course, Employee, Salarylog,EmployeeImage
from .serializers import StudentSerializer,CourseSerializer,EmployeeSerializer, SalarylogSerializer
from rest_framework.decorators import api_view
from django.db import transaction
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from urllib.parse import urlparse
from rest_framework import status
from .pagination import StudentPagination,EmployeePagination,EmployeeCursorPagination
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
@api_view(['POST'])
@transaction.atomic
def create_employee(request):   
    try:
        name=request.data.get("emp_name")
        salary=request.data.get("emp_salary")
        images=request.FILES.getlist("emp_img")
        new_img=[]
        
        if name is None:
            return Response({
                    "status":"Failed",
                    "message":"Please Provide requierd fileds name",
                },status=status.HTTP_404_NOT_FOUND)
        
        if  salary is None:
            return Response({
                    "status":"Failed",
                    "message":"Please Provide requierd fileds salary",
                },status=status.HTTP_404_NOT_FOUND)
        
        if not isinstance(name,str):
            return Response({   
                "status":"Failed",
                "message":"Name must be String",
            },status=status.HTTP_404_NOT_FOUND)
        
        employee=Employee.objects.create(emp_name=name,emp_salary=salary)

        for image in images:
            img=EmployeeImage.objects.create(employee=employee,images=image)
            new_img.append(request.build_absolute_uri((img.images.url)) if img else None)


        Salarylog.objects.create(employee=employee,amount=salary)
        
        return Response({
            "status":"Sucessfully",
            "message":"Created Employee Detail",
        },status=status.HTTP_201_CREATED)
    
    except Exception as e :
        return Response({
            "status" :"Error",
            "messge": str(e),
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
@api_view(['GET'])
def fetch_cursor_employee(request):
    try:
        employee = Employee.objects.all()
        paginator=EmployeeCursorPagination()
        padinated_employee=paginator.paginate_queryset(employee,request)
        new_employee=[]

        for item in padinated_employee:
            image=[]
            for img in item.images.all():
                image.append(request.build_absolute_uri(img.images.url))

            data_dict={
                "ID":item.emp_id,
                "Name":item.emp_name,
                "Salary":item.emp_salary,
                "Image":image
            }

            new_employee.append(data_dict)


        return paginator.get_paginated_response({
            "Status": "Success",
            "Data": new_employee
        }) 

    except Exception as e:
        return Response({
            "status":"Error",
            "messsage":str(e),
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def fetch_employee(request):
    try:
        page_number =request.query_params.get('page',1)       
        page_size= request.query_params.get('page_size',3)  

        try:
            page_number = int(page_number)
            page_size = int(page_size)

        except ValueError:
            return Response({
                "status" : "failed", 
                "message" : "Page_number and page_size must be integer"},
                status=status.HTTP_400_BAD_REQUEST)
        
        if page_number <= 0 or page_size <= 0:
            return Response({
                "status":"failed" ,
                "message":"Page and page_size must be greater than 0"
                },status=status.HTTP_400_BAD_REQUEST)
        
        employee = Employee.objects.all()

        if not employee.exists():
            return Response({
                "Status":  "Failed",
                "Message": "No employees found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        try: 
            paginator=EmployeePagination()
            paginator.page_size=min(page_size, paginator.max_page_size)
            paginated_employee = paginator.paginate_queryset(employee, request)
        except:
            return Response({
                "status":"failed" ,
                "message": "Page number out of range"
                },status=status.HTTP_404_NOT_FOUND)

        if paginated_employee is None:            
            paginated_employee= list(employee)

        new_employee=[]
        for item in paginated_employee:
            image=[]
            for img in item.images.all():
                image.append(request.build_absolute_uri(img.images.url))

            data_dict={
                "ID":item.emp_id,
                "Name":item.emp_name,
                "Salary":item.emp_salary,
                "Image":image
            }

            new_employee.append(data_dict)


        return paginator.get_paginated_response({
            "status": "Success",
            "data": new_employee
        }) 

    except Exception as e:
        return Response({
            "status":"Error",
            "message":str(e),
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def search_employee(request):
    try:
        emp_id=request.data.get("emp_id")
        emp_name= request.data.get("emp_name")
        employees=Employee.objects.prefetch_related('images').all()

        if emp_id:
            employees= employees.filter(emp_id=emp_id)

        elif emp_name:
            employees= employees.filter(emp_name=emp_name)

        if not employees.exists():
            return Response({
                "status": "Failed",
                "message": "Employee Not Found",
            }, status=status.HTTP_404_NOT_FOUND)

        employee_data = []

        images=[]
        for employee in employees:
            for img in employee.images.all():
                images.append(request.build_absolute_uri(img.images.url))
             

            employee_data.append({
                "Id": employee.emp_id,
                "Name": employee.emp_name,
                "Salary": employee.emp_salary,
                "Images": images
            })

        return Response({
            "status":"Success",
            "message":"Search Successful",
            "data":employee_data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status":"Error",
            "message":str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT','PATCH'])
@transaction.atomic
def update_employee(request):
    try:
        id=request.data.get('emp_id')

        if not id:
            return Response({
                "status":"Failed",
                "message":"Please Provide requer field(id)"
            },status=status.HTTP_404_NOT_FOUND)
        
        employee=Employee.objects.get(emp_id=id)
        employee.emp_name=request.data.get('emp_name')
        employee.emp_salary=request.data.get('emp_salary')
        img=request.FILES.getlist('emp_img')
        update_img=[]

        for i  in img:
            new_img=EmployeeImage(employee=employee,images=i)
            update_img.append(new_img)
        
        EmployeeImage.objects.bulk_create(update_img)

        employee.save()

        return Response({
            'status':"Successfully",
            "message":"Updated Sucessully",
        },status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            "status":"Error",
            "message":str(e),
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['DELETE'])
def delete_employee(request):
    try:
        name = request.data.get("emp_name")
        id = request.data.get("emp_id")

        if id is None:
            return Response({
                "status":"Failed",
                "message":"Provide requir fileld  id",
            })
        
        
        employee=Employee.objects.get(emp_id=id)

        employee.delete()
      
        return Response({
            "status":"Deleted Sucesfully",
            "message":"Remove {employee.emp_name}Employee",
        },status=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        return Response({
            "status":"Error",
            "message":str(e),
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
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

        paginator=StudentPagination()
        paginated_student=paginator.paginate_queryset(students,request)

        serializer=StudentSerializer(paginated_student,many=True)

        return paginator.get_paginated_response({
            "Status": "Success",
            "Data": serializer.data
        })
    
    except Exception as e:
        return Response({
            "Status" : "Failed",
            "Errors" : str(e)
        },status=status.HTTP_400_BAD_REQUEST)

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



