from email.headerregistry import Address
from django.db import models

#from Handler.views import Categories

class Teacher_Info(models.Model):
    User = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    Full_Name = models.CharField(max_length=100)
    Location = models.CharField(max_length=100, null=True)
    Email = models.EmailField(max_length=100)
    Type = models.CharField(max_length=100)
    Contact = models.CharField(max_length=100, null=True)
    School_Name = models.CharField(max_length=100, null=True)
    School_Type = models.CharField(max_length=100, null=True)
    School_Descriptions = models.CharField(max_length=2000, null=True)
    Plans = models.CharField(max_length=100, null=True)
    Currency = models.CharField(max_length=100, null=True)
    Last_Seen = models.CharField(max_length=100, null=True)
    Days_Left = models.CharField(max_length=100, null=True)
    Verify = models.CharField(max_length=100, null=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.User
    
class Student_Info(models.Model):
    User = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    Full_Name = models.CharField(max_length=100)
    Location = models.CharField(max_length=100, null=True)
    Email = models.EmailField(max_length=100)
    Type = models.CharField(max_length=100)
    Contact = models.CharField(max_length=100, null=True)
    Last_Seen = models.CharField(max_length=100, null=True)
    Days_Left = models.CharField(max_length=100, null=True)
    Verify = models.CharField(max_length=100, null=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.User    
    
class Cookie_Handler(models.Model):
    Cookie = models.CharField(max_length=100)
    User = models.IntegerField()
    Type = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)   
    def __str__(self):
        return self.Cookie  

class Course_Info(models.Model):
    Name = models.CharField(max_length=100)
    User = models.IntegerField()
    Type = models.CharField(max_length=100)
    Level = models.CharField(max_length=100)
    Amount = models.CharField(max_length=100)
    Rate = models.CharField(max_length=100, null=True)
    Interest = models.CharField(max_length=100, null=True)
    Sales = models.CharField(max_length=100, null=True)
    Description = models.CharField(max_length=5000)
    date = models.DateField(auto_now_add=True)   
    def __str__(self):
        return self.Name   


class Topic_Info(models.Model):
    Name = models.CharField(max_length=100)
    User = models.IntegerField()
    Module = models.IntegerField()
    Course = models.IntegerField()
    Level = models.CharField(max_length=100)
   # Description = models.CharField(max_length=5000)
    date = models.DateField(auto_now_add=True)   
    def __str__(self):
        return self.Name

class Topic_Question(models.Model):
    Topic = models.CharField(max_length=100)
    User = models.IntegerField()
    Question = models.CharField(max_length=1000)
    A_answer = models.CharField(max_length=1000)
    B_answer = models.CharField(max_length=1000)
    C_answer = models.CharField(max_length=1000)
    D_answer = models.CharField(max_length=1000)
    Answer = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)   
    def __str__(self):
        return self.Question  

class Topic_Link(models.Model):
    Topic = models.CharField(max_length=100)
    User = models.IntegerField()
    Link = models.CharField(max_length=1000)
    Description = models.CharField(max_length=1000)
    Name = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True)   
    def __str__(self):
        return self.Name
    
class Video_Link(models.Model):
    Topic = models.CharField(max_length=100)
    User = models.IntegerField()
    Link = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True)   
    def __str__(self):
        return self.Link

class Student_Courses(models.Model):
    Course = models.CharField(max_length=100)
    User = models.IntegerField()
    Student = models.IntegerField()
    Level = models.CharField(max_length=100)
    Type = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)   
    def __str__(self):
        return self.Level

class Test_Taken(models.Model):
    Student = models.IntegerField()
    Topic = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)   
    def __str__(self):
        return self.Topic

class Student_Result(models.Model):
    Test = models.CharField(max_length=100)
    Student = models.IntegerField()
    Question = models.CharField(max_length=100)
    Status = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)   
    def __str__(self):
        return self.Status


class Notifications(models.Model):
    Uid = models.IntegerField()
    Info = models.CharField(max_length=1000)
    Type = models.CharField(max_length=100)
    Status = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)   
    def __str__(self):
        return self.Status
    

class Verify(models.Model):
    User = models.IntegerField()
    Uid = models.CharField(max_length=1000)
    Type = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)   
    def __str__(self):
        return self.Type
    
class Admin_Info(models.Model):
    User = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    Name = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True)   
    def __str__(self):
        return self.Name
    
class Module_Info(models.Model):
    Course = models.CharField(max_length=100) 
    date = models.DateField(auto_now_add=True)   
    def __str__(self):
        return self.Course