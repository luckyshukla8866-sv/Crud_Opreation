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
    
class Employee(models.Model):
    emp_id=models.AutoField(primary_key=True)
    emp_name=models.CharField(max_length=100)
    emp_salary=models.IntegerField()
    img=models.ImageField(upload_to='employees/')

    def __str__(self):
        return self.emp_name
    
class Salarylog(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    amount=models.ImageField()

    def __str__(self):
        return self.amount
    