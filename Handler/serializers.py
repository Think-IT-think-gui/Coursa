from rest_framework import serializers
from . models import Teacher_Info,Student_Info



class Teacher_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher_Info
        fields = '__all__'

class Student_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Student_Info
        fields = '__all__'