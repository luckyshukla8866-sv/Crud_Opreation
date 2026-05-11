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
                    "Status":"Failed",
                    "Message":"Please Provide requierd fileds name",
                    "Data":"Not Found"
                })
        
        if  salary is None:
            return Response({
                    "Status":"Failed",
                    "Message":"Please Provide requierd fileds salary",
                    "Data":"Not Found"
                })
        
        if not isinstance(name,str):
            return Response({   
                "Status":"Failed",
                "Message":"Name must be String",
                "Data":"Not Found"
            })
        
        employee=Employee.objects.create(emp_name=name,emp_salary=salary)

        for image in images:
            img=EmployeeImage.objects.create(employee=employee,images=image)
            new_img.append(request.build_absolute_uri((img.images.url)) if img else None)


        Salarylog.objects.create(employee=employee,amount=salary)
        
        return Response({
            "Status":"Sucessfully",
            "Message":"Created Employee Detail",
            "Data":{
                "Name":employee.emp_name,
                    "Image":new_img
            }
        },status=status.HTTP_201_OK)
    
    except Exception as e :
        return Response({
            "Status" :"Failed",
            "Messge": str(e),
            "Data":"Not Found"
        }) 

@api_view(['GET'])
def fetch_employee(request):
    try:
        employee = Employee.objects.all()
        
        new_employee=[]
        for item in employee:
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

        return Response({
            "Status":"Successfully",
            "Message":"Employee Detail",
            "Data":new_employee
        },status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "Status":"Failed",
            "Messsage":str(e),
            "Data":"Not Found"
        })


@api_view(['POST'])
def search_employee(request):
    try:
        id=request.data.get("emp_id")
        name=request.data.get("emp_name")

        new_dict={}
        employee=Employee.objects.all()
        

        print("Step2")
        print(employee)

        if id is not None:
            # if name == "":
            #     return Response({
            #         "Status":"Failed",
            #         "Message":"Please provide requer id",
            #         "Data":"Not Found"
            #     })

            print("Step3")
            employee=Employee.objects.filter(emp_id=id)
            print("Step4")
            image=[]
            for items in employee:
                    print("Step5")
                    for img in items.images.all():
                        print("Step6")
                        if items.emp_id == img.img_id:
                            
                            image.append(request.build_absolute_uri(img.images.url))

                    data_dict={
                        "Id":items.emp_id,
                        "Name":items.emp_name,
                        "Salary":items.emp_salary,
                        "Images":image
                    }
                    print("Step7")
            print(data_dict)
            
        
            return Response({
                "Status":"Search sucessfully",
                "data":data_dict,
            },status.HTTP_200_OK) 
                    

        elif name is not None:
            # if name == "":
            #     return Response({
            #         "Status":"Failed",
            #         "Message":"Please provide requer name",
            #         "Data":"Not Found"
            #     })
            

            employee=Employee.objects.filter(emp_name=name)
            image=[]
            for items in employee :
                for img in items.images.all():
                    if items.emp_id == img.img_id:
                        image.append(request.build_absolute_uri(img.images.url))
                        
                data_dict={
                    "Id":employee.emp_id,
                    "Name":employee.emp_name,
                    "Salary":employee.emp_salary,
                    "Images":image
                }
                print(data_dict)
        
            return Response({
                "Status":"Search sucessfully",
                "data":data_dict,
            },status.HTTP_200_OK) 
            
        
        new_employee=[]
        for item in employee:
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
                

        return Response({
            "Message":"Search Sucessfull", 
            "Data":new_employee
        },status.HTTP_200_OK)
    
    except Employee.DoesNotExist:
        return Response({
            "Status":"Failed",
            "message":"Employee Not Found",
            "Data":"Not Found"
        })
    
    except Exception as e:
        return Response({
            "Status":"Falied",
            "Message":str(e),
            "Data":"Not Found"
        })


@api_view(['PUT','PATCH'])
@transaction.atomic
def update_employee(request):
    try:
        id=request.data.get('emp_id')

        if not id:
            return Response({
                "Status":"Failed",
                "Data":"Please Provide requer field(id)"
            })
        
        employee=Employee.objects.get(emp_id=id)
        employee.emp_name=request.data.get('emp_name')
        employee.emp_salary=request.data.get('emp_salary')
        img=request.FILES.getlist('emp_img')
        update_img=[]

        for i  in img:
            new_img=EmployeeImage(employee=employee,images=i)
            update_img.append(new_img)
        
        EmployeeImage.objects.bulk_create(update_img)

        print("Step 2")
        employee.save()

        return Response({
            'Status':"Successfully",
            "Message":"Updated Sucessully",
            "Data":"Done"
        },status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            "Status":"Failed",
            "Message":str(e),
            "Data":"Not Found"
        })



@api_view(['DELETE'])
def delete_employee(request):
    try:
        name = request.data.get("emp_name")
        id = request.data.get("emp_id")

        if id is None:
            return Response({
                "Status":"Failed",
                "Message":"Provide requir fileld  id",
                "Data":"Not Found"
            })
        
        
        employee=Employee.objects.get(emp_id=id)

        employee_data={
            "Data":{
                "Id":employee.emp_id,
                "Name":employee.emp_name
            }
        }

        employee.delete()
      
        return Response({
            "Status":"Deleted Sucesfully",
            "Message":"Remove {employee.emp_name}Employee",
            "Data": employee_data
        },status=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        return Response({
            "Status":"Failed",
            "Message":str(e),
            "Data":"Not found"
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



