from rest_framework import serializers
from  .models import Student,Course,Employee,Salarylog


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = Course
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(source='course_set', many=True, read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "name",
            "age",
            "email",
            'courses'
        ]

class EmployeeSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(use_url=True)
    class Meta:
        model=Employee
        fields= '__all__'

class SalarylogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salarylog
        fields='__all__'



        