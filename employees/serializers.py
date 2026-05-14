from rest_framework import serializers
from  .models import Employee,Salarylog


class SalarylogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salarylog
        fields='__all__'

        