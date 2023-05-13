from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from . serializers import Teacher_Serializer,Student_Serializer
from . models import Teacher_Info,Student_Info,Cookie_Handler,Course_Info,Topic_Link,Topic_Info,Topic_Question,Video_Link,Student_Courses,Test_Taken,Student_Result,Notifications,Module_Info
from rest_framework.response import Response
from rest_framework.views import APIView
from pathlib import Path
from django.core.files.storage import FileSystemStorage
import os
from django.db.models import Q
import shutil
from time import *
import uuid
import random
import math
import email, smtplib, ssl
from tkinter import filedialog
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from django.utils.translation import gettext as _
BASE_DIR = Path(__file__).resolve().parent.parent


#===================================================== Buy Course ===========================================================

class Bought_Courses_Content(APIView):
    def post(self , request):
      courses = Course_Info.objects.all()
      selected =  Course_Info.objects.get(id= int(request.data["id"]))
      topic = Topic_Info.objects.filter(Course=int(request.data["id"])) 
      Module = Module_Info.objects.filter(Course=int(request.data["id"]))
      module = []
      count = 0
      for i in Module:
        count +=1
        module.append({
          "id":i.id,"Number": count,"date":i.date
        })

      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
           return redirect('home')
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
          
          return render(request , "home/course-details.html", {"Courses":courses[0:3],"Selected":selected,"Data":User_data,"Module":module,"Topic":topic,"Inscpect":"Yes"})
         except:
           pass
      no_users = {"Type":"None"}
     
      return render(request , "home/course-details.html", {"Courses":courses[0:3],"Selected":selected,"Data":no_users,"Module":module,"Topic":topic,"Inscpect":"Yes"})
      


class Buy(APIView):
    def post(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           return redirect('home')
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           Notifications.objects.create(Status = "New",Uid = User_data.id, Type="Student", Info=f"You have successfully bought a course, check your dashboard for feedback.")
          try:
            Student_Courses.objects.get(Student=User_data.id,Course=int(request.data["id"])) 
            return redirect("teacher_dashboard")
          except:
            user = Course_Info.objects.get(id=int(request.data["id"]))
            Student_Courses.objects.create(Student=User_data.id,Course=int(request.data["id"]),Level="0",User=user.User) 
            return redirect("teacher_dashboard") 
         except:
            return redirect('home')
      return redirect('home')
#===================================================== Buy Course ===========================================================

#====================================================== Learn / Tests =========================================================
class Learn_Courses(APIView):
    def post(self , request):
      
      selected =  Topic_Info.objects.get(id= int(request.data["id"]))   
      if 'csrf-session-xdii-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-session-xdii-token']
        # try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           return redirect('home')
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
          Video = Video_Link.objects.get(Topic=request.data["id"]) 
          questions = Topic_Question.objects.filter(Topic=request.data["id"])
          q_data = []
          count = 0
          for i in questions:
            count+=1
            q_data.append({
              "id":i.id,"Question":i.Question,"Number":count,"A_answer":i.A_answer,"B_answer":i.B_answer,"C_answer":i.C_answer,"D_answer":i.D_answer
            })
          links = Topic_Link.objects.filter(Topic=request.data["id"])
          topic_info = Topic_Info.objects.get(id = int(request.data["id"]))
          Course = Course_Info.objects.get(id=int(topic_info.Course))
          Topics = Topic_Info.objects.filter(Course= Course.id)

          return render(request , "Temp_1/topic-learn.html", {"Selected":selected,"Data":User_data,"Topic":Topics,"Video":Video,"Questions":q_data,"Links":links,"Course":Course})
         #except:
         #  return redirect('home')
      return redirect('home')
    

class Take_Test(APIView):
    def post(self , request):
     # print(request.data)
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
           return Response("Teacher") 
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           
          Test_Taken.objects.create(Student=User_data.id,Topic=request.data["Topic"])
          current_test = Test_Taken.objects.last()

          for i in request.data:
            if i == "Topic":
              pass
            else:
             print(request.data[i]["id"])
             checking = Topic_Question.objects.get(id= int(request.data[i]["id"]))
             if checking.Answer == request.data[i]["Value"]:
              stat = "Correct"
             else:
              stat = "Wrong"  
             Student_Result.objects.create(Student=User_data.id,Test=current_test.id,Question=request.data[i]["id"],Status = stat)
             Notifications.objects.create(Status = "New",Uid = User_data.id, Type="Student", Info=f"You have successfully submited your test, check your results board for feedback.")
          return Response("Done")  
         except:
           return redirect("login")
      return Response("login")


class Results_View(APIView):
    def post(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           return redirect('home')

          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           
          #current_date = strftime("%Y-%m-%d")
          results = Test_Taken.objects.filter(Student=User_data.id)
          listed = []
          count = 0
          for i in results:
            count +=1
            listed.append({
              "id":i.id,"Number":count,"date":i.date
            })
          notify = Notifications.objects.filter(Uid=User_data.id,Type="Student")
          return render(request , "Temp_2/results.html", {"Data":User_data,"Results":listed,"Notify":notify})
         except:
           return redirect('home')
      return redirect('home')
    
class Results(APIView):
    def post(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           return redirect('home')

          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           
          #current_date = strftime("%Y-%m-%d")
          results = Student_Result.objects.filter(Student=User_data.id,Test=request.data["id"])
          listed = []
          count = 0
          Correct = 0
          for i in results:
            count +=1
            if i.Status == "Correct":
              Correct +=1
            listed.append({
              "id":i.id,"Number":count,"Status":i.Status,
            })
          stat = (Correct/count)*100
          if stat > 50 :
            remark = "Passed"
          else:
            remark = "Failed"   
            
            
          test = Test_Taken.objects.get(id= int(request.data["id"]))  
          notify = Notifications.objects.filter(Uid=User_data.id,Type="Student")
          return render(request , "Temp_2/view_results.html", {"Data":User_data,"Results":listed,"Remark":remark,"Date":test.date,"Mark":round(stat,2),"Notify":notify})
         except:
           return redirect('home')
      return redirect('home')
#====================================================== Learn / Tests =========================================================
   