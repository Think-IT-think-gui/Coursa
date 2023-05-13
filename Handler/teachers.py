from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.urls import reverse
from . serializers import Teacher_Serializer,Student_Serializer
from . models import Teacher_Info,Student_Info,Cookie_Handler,Module_Info,Course_Info,Topic_Link,Topic_Info,Topic_Question,Video_Link,Student_Courses,Test_Taken,Student_Result,Notifications
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




#========================================== Course ==========================================================
class Create_Course(APIView):
    def get(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           return Response("Student")
          #current_date = strftime("%Y-%m-%d")
          notify = Notifications.objects.filter(Uid=User_data.id,Type="Teacher")
          
          return render(request , "Temp_2/create_course.html", {"Data":User_data,"Notify":notify})
         except:
           return redirect('home')
      return redirect('home')   
    def post(self, request):
      if 'csrf-session-xdii-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-session-xdii-token']
        # try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           return Response("Student")
          #current_date = strftime("%Y-%m-%d")
          prefixed = request.data
          Course_Info.objects.create(User=User_data.id,Name=prefixed["Name"],Type=prefixed["Type"],Amount=prefixed["Amount"],Description=prefixed["Description"],Level=prefixed["Level"],Rate="0.0",Interest="0",Sales="0")
          course = Course_Info.objects.last()
          uploading_file = request.FILES['New_Img']
          fs = FileSystemStorage()
          fs.save("Courses//"+str(course.id)+".jpg",uploading_file)
          print("ff")
          uploading_file2 = request.FILES['video']
          fs = FileSystemStorage()
          fs.save("Intros//"+str(course.id)+".mp4",uploading_file2)
          Notifications.objects.create(Status = "New",Uid = User_data.id, Type="Teacher", Info=f"You have successfully created a new course.")

          return redirect(reverse('module_page',kwargs={"pk":course.id}))
         #except:
        #   return redirect('home')
      return redirect('home') 

class Edith_Course(APIView):
    def get(self , request,pk):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           return Response("Student")
          #current_date = strftime("%Y-%m-%d")
          notify = Notifications.objects.filter(Uid=User_data.id,Type="Teacher")
          info = Course_Info.objects.get(id = int(pk))
          return render(request , "Temp_2/edith_course.html", {"Data":User_data,"Notify":notify,"Info":info})
         except:
           return redirect('home')
      return redirect('home')   
    def post(self, request,pk):
      if 'csrf-session-xdii-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-session-xdii-token']
        # try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           return Response("Student")
          #current_date = strftime("%Y-%m-%d")
          prefixed = request.data
          Course_Info.objects.filter(id=int(prefixed["Course"])).update(Name=prefixed["Name"],Type=prefixed["Type"],Amount=prefixed["Amount"],Description=prefixed["Description"],Level=prefixed["Level"])
          course = Course_Info.objects.get(id=int(prefixed["Course"]))
          try:
           os.remove(f'{BASE_DIR}/media/Courses/{course.id}.jpg')
           uploading_file = request.FILES['New_Img']
           fs = FileSystemStorage()
           fs.save("Courses//"+str(course.id)+".jpg",uploading_file)
           print("ff")
          except:
            pass 
          try:
           os.remove(f'{BASE_DIR}/media/Intros/{course.id}.mp4')
           uploading_file2 = request.FILES['video']
           fs = FileSystemStorage()
           fs.save("Intros//"+str(course.id)+".mp4",uploading_file2)
          except:
            pass
          Notifications.objects.create(Status = "New",Uid = User_data.id, Type="Teacher", Info=f"You have successfully created a new course.")

          return redirect(reverse('module_page',kwargs={"pk":course.id}))
         #except:
        #   return redirect('home')
      return redirect('home') 

class Course_Update(APIView):
    def get(self , request, pk):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           return Response("Student")
          Topics = Topic_Info.objects.filter(Module = pk)
          co = Module_Info.objects.get(id = int(pk) )
          notify = Notifications.objects.filter(Uid=User_data.id,Type="Teacher")

          return render(request , "Temp_2/topics.html", {"Data":User_data,"Course":co.Course,"Module":pk,"Topic":Topics,"Notify":notify})
         except:
           return redirect('home')
      return redirect('home')
    
class Create_Module(APIView):
    def post(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-session-xdii-token']
        # try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           return Response("Student")
          Module_Info.objects.create(Course=request.data["id"])
          return redirect(reverse('module_page',kwargs={"pk":request.data["id"]}))
        # except:
         #  return redirect('home')
      return redirect('home')
    

class Module_Page(APIView):
    def get(self , request,pk):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           return Response("Student")
          #current_date = strftime("%Y-%m-%d")
          Topics = Module_Info.objects.filter(Course = pk)
          listed = []
          num = 0
          for i in Topics:
            num += 1
            listed.append({
              "id":i.id,"count":num
            })
          notify = Notifications.objects.filter(Uid=User_data.id,Type="Teacher")

          return render(request , "Temp_2/module.html", {"Data":User_data,"Course":pk,"Topic":listed,"Notify":notify})
         except:
           return redirect('home')
      return redirect('home')
#========================================== Course ==========================================================
    

#============================================= Topic ========================================================
class Create_Topic(APIView):
    def get(self , request,pk):
      if 'csrf-session-xdii-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-session-xdii-token']
         #try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           return Response("Student")
          #current_date = strftime("%Y-%m-%d")
          courses = Course_Info.objects.filter(User=User_data.id)
          Questions = Topic_Question.objects.filter(Topic=pk)
          Links = Topic_Link.objects.filter(Topic=pk)
          notify = Notifications.objects.filter(Uid=User_data.id,Type="Teacher")
          return render(request , "Temp_2/create_topic.html", {"Data":User_data,"Courses":courses,"Topic":pk,"Questions":Questions,"Links":Links,"Notify":notify})
        # except:
          # return redirect('home')
      return redirect('home')
    
class Add_Topic(APIView):
    def post(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
          user1_check = request.COOKIES['csrf-session-xdii-token']
        # try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           return Response("Student")
        
          Topic_Info.objects.create(User=User_data.id,Course = request.data["Course"], Name= request.data["Name"],Level = request.data["Level"],Module= request.data["Module"])
          data = Topic_Info.objects.last()
          rand_int =  random.randint(1,10)
          shutil.copyfile(f"{BASE_DIR}/static/Default/users/{rand_int}.jpg", f"{BASE_DIR}/media/Topics/{str(data.id)}.jpg")
          Notifications.objects.create(Status = "New",Uid = User_data.id, Type="Teacher", Info=f"You have successfully created a topic.")

          
          return redirect(reverse('create_topic',kwargs={"pk":data.id}))
        # except:
         #  return redirect('home')
      return redirect('home')

class Topic_Config(APIView):
    def post(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           return Response("Student")
          print(request.data)
          if request.data["video"] == '':
            pass
          else:
            try: 
             linked = Video_Link.objects.get(Topic = request.data["Topic"])
             os.remove(f'{BASE_DIR}/media/Videos/{linked.Link}.mp4')
             link = linked.Link
            except:
              link = uuid.uuid1()
              Video_Link.objects.create(User=User_data.id,Link=link,Topic=request.data["Topic"])
            uploading_file = request.FILES['video']
            fs = FileSystemStorage()
            fs.save("Videos//"+str(link)+".mp4",uploading_file) 
          if request.data["New_Img"] == '':
           pass
          else:
           try:
            os.remove(f'{BASE_DIR}/media/Topics/{request.data["Topic"]}.jpg')
           except:
             pass
           uploading_file = request.FILES['New_Img']
           fs = FileSystemStorage()
           fs.save("Topics//"+str(request.data["Topic"])+".jpg",uploading_file)  
          Notifications.objects.create(Status = "New",Uid = User_data.id, Type="Teacher", Info=f"You have successfully made changes to your course.")
          return redirect(reverse('create_topic',kwargs={"pk":request.data["Topic"]}))
         except:
           return redirect('home') 
      return redirect('home')
#============================================= Topic ========================================================


#================================================ Question =================================================
class Add_Question(APIView):
    def post(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           return Response("Student")
          print(request.data)
          Topic_Question.objects.create(
            User=User_data.id,Topic = request.data["Topic"],
            Question= request.data["Question"],A_answer = request.data["A_answer"],
            B_answer = request.data["B_answer"],C_answer = request.data["C_answer"],
            D_answer = request.data["D_answer"],Answer = request.data["Answer"])
          id = Topic_Question.objects.last()
          val=  {"Status":"added","id":id.id}
          Notifications.objects.create(Status = "New",Uid = User_data.id, Type="Teacher", Info=f"You have successfully added a question.")

          return Response(val)
         except:
           return redirect('home')
      return Response("login")



class Add_Link(APIView):
    def post(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           return Response("Student")
          print(request.data)
          Topic_Link.objects.create(
            User=User_data.id,Topic = request.data["Topic"],Name= request.data["Name"],Link= request.data["Link"],Description= request.data["Description"])
          id = Topic_Link.objects.last()  
          val ={"Status":"added","id":id.id}
          Notifications.objects.create(Status = "New",Uid = User_data.id, Type="Teacher", Info=f"You have successfully added a link.")

          return Response(val)
         except:
           return redirect('home')
      return Response("login")

class Delete_Request(APIView):
    def post(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           return Response("Student")
          print(request.data)
          if request.data["Type"] == "Link":
            Topic_Link.objects.get(id=int(request.data["id"])).delete()
            Notifications.objects.create(Status = "New",Uid = User_data.id, Type="Teacher", Info=f"You have successfully deleted your link.")

          else:
            Topic_Question.objects.get(id=int(request.data["id"])).delete()  
            Notifications.objects.create(Status = "New",Uid = User_data.id, Type="Teacher", Info=f"You have successfully deleted your question.")
          return Response("Deleted")
         except:
           return redirect('home')
      return Response("login")
#================================================ Question =================================================



#============================================ List Students ==================================================
class List_Students(APIView):
    def get(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           return redirect("teacher_dashboard")
          listed = []
          Sales = Student_Courses.objects.filter(User=User_data.id)
          for i in Sales:
            data = Student_Info.objects.get(id =int(i.Student))
            listed.append({
              "id":data.id,"Name":data.Full_Name,"Email":data.Email,"Contact":data.Contact,"Location":data.Location,"date":i.date
            })
          notify = Notifications.objects.filter(Uid=User_data.id,Type="Teacher")
          return render(request, 'Temp_2/Students_info.html',{"Data":User_data,"Listed":listed,"Notify":notify})
         except:
           return redirect('home')
      return redirect('home')

#============================================ List Students ==================================================
