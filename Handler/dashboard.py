from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from . serializers import Teacher_Serializer,Student_Serializer
from . models import Teacher_Info,Student_Info,Cookie_Handler,Course_Info,Topic_Link,Topic_Info,Topic_Question,Video_Link,Student_Courses,Test_Taken,Student_Result,Notifications
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


class Main_Dashboard(APIView):
    def get(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
           num_couses = 0
           num_sales = 0
           num_assigments = 0
           num_links = 0
           course_date = "No Activity"
           sale_date = "No Activity"


           courses_info = Course_Info.objects.filter(User=User_data.id)
           for i in courses_info:
             num_couses += 1
             course_date = i.date
           sale_info = Student_Courses.objects.filter(User = User_data.id)
           for i in sale_info:
             num_sales +=1
             sale_date = i.date
           assigments_info = Topic_Question.objects.filter(User=User_data.id)
           for i in assigments_info:
             num_assigments += 1
           link_info = Topic_Link.objects.filter(User=User_data.id)
           for i in link_info:
             num_links += 1  
           try: 
            per_assigment = (num_assigments/(num_assigments+num_links))*100
            per_link = 100 - per_assigment
           except:
             per_assigment = 0
             per_link = 0
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           bougth = Student_Courses.objects.filter(Student=int(find.User))

           listed=[]
           for i in bougth:
             course = Course_Info.objects.get(id= int(i.Course))
             listed.append({
               "id":course.id,"Name":course.Name,
               "Rate":course.Rate,"date":course.date,
               "Level":course.Level,"Done":i.Level,
               "Interest":course.Interest,
               "Amount":course.Amount,
               "Type": i.Type
             })
           num_course = 0
           num_assigment = 0
           num_passed = 0
           num_failed = 0
           
           sale_dated = "No Activity" 
           sale_info = Student_Courses.objects.filter(Student = User_data.id)
           for i in sale_info:
             num_course +=1
             sale_dated = i.date

             assigments_info = Topic_Question.objects.filter(User=int(i.User))
             for i in assigments_info:
              num_assigment += 1
           Tests = Student_Result.objects.filter(Student=User_data.id)
           for i in Tests:
            if i.Status == "Correct":  
             num_passed += 1
            else:
              num_failed += 1
           try: 
            per_passed = (num_passed/(num_passed+num_failed))*100
            per_failed = 100 - per_passed
           except:
             per_passed = 0
             per_failed = 0
           
 



           notify = Notifications.objects.filter(Uid=User_data.id,Type="Student")
           
           return render(request , "Temp_2/student.html", {
                        "Data":User_data,"Courses":listed,
                        "Number_couses":num_course,"Dated":sale_dated,
                        "Number_assignment":num_assigment,
                        "Passed":num_passed,"Failed":num_failed,
                        "Passed_percent":round(per_passed,2),
                        "Failed_percent":round(per_failed,2),
                        "Notify":notify
                        })
          #current_date = strftime("%Y-%m-%d")
          courses = Course_Info.objects.filter(User=User_data.id)
          notify = Notifications.objects.filter(Uid=User_data.id,Type="Teacher")

          return render(request , "Temp_2/dashboard.html", {
                         "Data":User_data,"Courses":courses,
                         "Number_course":num_couses,"Number_sale":num_sales,
                         "Number_assigment":num_assigments,"Number_link":num_links,
                         "Link_percent":round(per_link,2),"Assignment_percent":round(per_assigment,2),
                         "Sale_date":sale_date,"Course_date":course_date,"Notify":notify
                         })
         except:
           return redirect('home')
      return redirect('home')