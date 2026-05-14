from django.db import models

# Create your models here.
     
class Employee(models.Model):
    emp_id=models.AutoField(primary_key=True)
    emp_name=models.CharField(max_length=100)
    emp_salary=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.emp_name
    
class EmployeeImage(models.Model):
    img_id=models.AutoField(primary_key=True)
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name="images")
    images=models.ImageField(upload_to='employees/')
    
class Salarylog(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    amount=models.ImageField()

    def __str__(self):
        return self.amount
    