from django.db import models

class Student(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.name

class Course(models.Model):
    course_name=models.CharField(max_length=100)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name


    