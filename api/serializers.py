from rest_framework import serializers
from  .models import Student,Course


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
        