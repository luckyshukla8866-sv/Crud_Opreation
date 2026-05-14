from django.shortcuts import render
from django.shortcuts import render
from rest_framework.response import Response
from .models import Employee, Salarylog,EmployeeImage
from .serializers import  SalarylogSerializer
from rest_framework.decorators import api_view
from django.db import transaction
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from rest_framework import status
from .pagination import EmployeePagination,EmployeeCursorPagination
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.views import APIView

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
                    "status":"failed",
                    "message":"please provide requierd fileds name",
                },status=status.HTTP_404_NOT_FOUND)
        
        if  salary is None:
            return Response({
                    "status":"failed",
                    "message":"please provide requierd fileds salary",
                },status=status.HTTP_404_NOT_FOUND)
        
        if not isinstance(name,str):
            return Response({   
                "status":"failed",
                "message":"name must be string",
            },status=status.HTTP_404_NOT_FOUND)
        
        employee=Employee.objects.create(emp_name=name,emp_salary=salary)

        for image in images:
            img=EmployeeImage.objects.create(employee=employee,images=image)
            new_img.append(request.build_absolute_uri((img.images.url)) if img else None)


        Salarylog.objects.create(employee=employee,amount=salary)
        
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

        data=paginator.get_paginated_response(new_employee)

        return Response({
            "status": "successfully",
            "message":"search Employee Detail",
            "data": data,
        },status=status.HTTP_200_OK) 

    except Exception as e:
        return Response({
            "status":"Error",
            "messsage":str(e),
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def fetch_employee(request):
    try:
        id=request.data.get('emp_id')
        search=request.data.get('search')
        page_number =request.data.get('page')       
        page_size= request.data.get('page_size')  
        start_date=request.data.get('start_date')
        end_date=request.data.get('end_date')
      
        if not page_number:
            return Response({
                "status":"failed",
                "message":"please provide requierd fileds(page)",
                },status=status.HTTP_400_BAD_REQUEST)
       
        if not page_size:
            return Response({
                "status":"failed",
                "message":"please provide requierd fileds(page_size)",
                },status=status.HTTP_400_BAD_REQUEST)
          
   
        try:
            page_number = int(page_number)
            page_size = int(page_size)

        except ValueError:
            return Response({
                "status" : "failed", 
                "message" : "page_number and page_size must be integer"},
                status=status.HTTP_400_BAD_REQUEST)
        
        print("Step 4")
        if page_number <= 0 or page_size <= 0:
            return Response({
                "status":"failed" ,
                "message":"page and page_size must be greater than 0"
                },status=status.HTTP_400_BAD_REQUEST)
        
        try:
            employees = Employee.objects.all()

        except Employee.DoesNotExist:
            return Response({
                "status":"failed",
                "message":"employee not found",
            },status=status.HTTP_404_NOT_FOUND)
        
        
        if id:
            employees = Employee.objects.filter(emp_id= id)
            print(employees)
        
        if search:
            employees = employees.filter(Q(emp_name__icontains = search) | Q(emp_salary__icontains = search) )

        if start_date and end_date:  
            employees=Employee.objects.filter(created_at__date__range=[start_date, end_date])

        #employees = employees.order_by('-created_at')

        paginator = Paginator(employees,page_size)
        try:
            paginator_data = paginator.page(page_number)
        except:
            return Response({
                "status":"failed" ,
                "message": "page number out of range"
                },status=status.HTTP_501_NOT_IMPLEMENTED)

        new_employee=[]
        for item in paginator_data:
            image=[]
            for img in item.images.all():
                image.append(request.build_absolute_uri(img.images.url))

            data_dict={
                "ID":item.emp_id,
                "Name":item.emp_name,
                "Salary":item.emp_salary,
                "Image":image,
                "Date":item.created_at.strftime("%Y-%m-%d %I:%M %p"),
            }

            new_employee.append(data_dict)

        

        return Response({
            "status":"success",
            "message":"Fetch student data...",
            "total_pages": paginator.num_pages,
            "current_page": page_number,
            "total_items": paginator.count,
            "employee":new_employee
            },
            status=status.HTTP_200_OK
            ) 

    except Exception as e:
        return Response({
            "status":"error",
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
                "status": "failed",
                "message": "employee not found",
            }, status=status.HTTP_404_NOT_FOUND)

        employee_data = []

        
        for employee in employees:
            images=[]
            for img in employee.images.all():
                images.append(request.build_absolute_uri(img.images.url))
             

            employee_data.append({
                "Id": employee.emp_id,
                "Name": employee.emp_name,
                "Salary": employee.emp_salary,
                "Images": images,
                "Date":employee.created_at.strftime("%Y-%m-%d %I:%M %p")
            })

        return Response({
            "status":"success",
            "message":"search successful",
            "data":employee_data
        }, status=status.HTTP_200_OK)

    except Employee.DoesNotExist:
        return Response({
            "status":"error",
            "message":"does not exist",
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({
            "status":"error",
            "message":str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT','PATCH'])
@transaction.atomic
def update_employee(request):
    try:
        id=request.data.get('emp_id')

        if not id:
            return Response({
                "status":"failed",
                "message":"please Provide requer field(id)"
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
            'status':"successfully",
            "message":"updated Sucessully",
        },status=status.HTTP_200_OK)
    
    except Employee.DoesNotExist:
        return Response({
            "status":"error",
            "message":"does not exist",
        }, status=status.HTTP_404_NOT_FOUND)
    
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
                "status":"failed",
                "message":"please Provide requer field(id)"
            },status=status.HTTP_404_NOT_FOUND)
        
        
        employee=Employee.objects.get(emp_id=id)
        print(employee)
        name=employee.emp_name
        employee.delete()
        print(name)

        return Response({
            "status":"deleted Sucesfully",
            "message":f"remove {name} Employee",
        },status=status.HTTP_200_OK)
    
    except Employee.DoesNotExist:
        return Response({
            "status":"failed",
            "message":"employee data not found",
        },status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "status":"error",
            "message":str(e),
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

