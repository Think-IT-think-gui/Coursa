from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from . serializers import Teacher_Serializer,Student_Serializer
from . models import Teacher_Info,Student_Info,Cookie_Handler,Course_Info,Topic_Link,Topic_Info,Topic_Question,Video_Link,Student_Courses,Test_Taken,Student_Result,Notifications,Verify,Module_Info
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





#=============================================== Home Page =================================================

class Landing(APIView):
    def get(self , request):
      courses = Course_Info.objects.all().reverse()
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))

          #current_date = strftime("%Y-%m-%d")
          
          return render(request , "home/index-1.html", {"Data":User_data,"Courses":courses[0:10],"Best":courses.reverse()[0:5]})
         except:
           pass
      no_users = {"Type":"None"}

      return render(request , "home/index-1.html", {"Data":no_users,"Courses":courses[0:10],"Best":courses.reverse()[0:5]})

#=============================================== Home Page =================================================

#================================================= View courses ============================================     
class Courses_Page(APIView):
    def get(self , request):
      courses = Course_Info.objects.all().reverse()
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try: 
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))

          #current_date = strftime("%Y-%m-%d")
          
          return render(request , "home/course.html", {"Data":User_data,"Courses":courses})
         except:
           pass
      no_users = {"Type":"None"}

      return render(request , "home/course.html", {"Data":no_users,"Courses":courses})


class Courses_Get(APIView):
    def get(self , request,pk):
      courses = Course_Info.objects.filter(Type=pk).all()
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try: 
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))

          #current_date = strftime("%Y-%m-%d")
          
          return render(request , "home/course.html", {"Data":User_data,"Courses":courses})
         except:
           pass
      no_users = {"Type":"None"}

      return render(request , "home/course.html", {"Data":no_users,"Courses":courses})


class Courses_Find(APIView):
    def post(self , request):
      courses = Course_Info.objects.filter(Type=request.data["Type"],Level=request.data["Level"]).all()
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try: 
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
          else:
           User_data = Student_Info.objects.get(id=int(find.User))

          #current_date = strftime("%Y-%m-%d")
          
          return render(request , "home/course.html", {"Data":User_data,"Courses":courses})
         except:
           pass
      no_users = {"Type":"None"}

      return render(request , "home/course.html", {"Data":no_users,"Courses":courses})
    


class Courses_Content(APIView):
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
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
          
          return render(request , "home/course-details.html", {"Courses":courses[0:3],"Selected":selected,"Data":User_data,"Module":module,"Topic":topic,"Inscpect":"No"})
         except:
           pass
      no_users = {"Type":"None"}
      return render(request , "home/course-details.html", {"Courses":courses[0:3],"Selected":selected,"Data":no_users,"Module":module,"Topic":topic,"Inscpect":"No"})
      
#================================================= view courses ============================================     


#===================================================== Login / Register / Logout ======================================
class Login(APIView):
    def get(self , request):
      return render(request , "Extra/Login.html")
    def post(self, request):
       current_time = strftime("%H:%M:%S %p")
       try: 
        if request.data["Type"] == "Teacher":
          data = Teacher_Info.objects.get(User=request.data['User'], Password=request.data['Password'])  
          response =  redirect('home')

          try:
            look_up = Cookie_Handler.objects.get(User=data.id, Type="Teacher")
            generated_uuid = look_up.Cookie
          except:
            generated_uuid = uuid.uuid1()
            Cookie_Handler.objects.create(User=data.id,Cookie = generated_uuid,Type="Teacher")
          response.set_cookie('csrf-session-xdii-token',generated_uuid)
          Notifications.objects.create(Status = "New",Uid = data.id, Type="Teacher", Info=f"You have successfully logged in on {current_time}.")
          return response 
        else:
          data = Student_Info.objects.get(User=request.data['User'], Password=request.data['Password'])  
          response =  redirect('home')
          try:
            look_up = Cookie_Handler.objects.get(User=data.id, Type="Student")
            generated_uuid = look_up.Cookie
          except:
            generated_uuid = uuid.uuid1()
            Cookie_Handler.objects.create(User=data.id,Cookie = generated_uuid,Type="Student")
          response.set_cookie('csrf-session-xdii-token',generated_uuid)
          Notifications.objects.create(Status = "New",Uid = data.id, Type="Student", Info=f"You have successfully logged in on {current_time}.")
          return response 
       except:
         return render (request, 'Temp_1/page-404.html' )


class Register(APIView):
    def get(self , request):
      return render(request , "Extra/Register.html")
    def post(self, request):
     
        if request.data["Type"] == "Teacher":
          try:
            Teacher_Info.objects.get(User=request.data['User'])  
            return render (request, 'Temp_1/page-404-2.html' )
          except:
             pass
          try:
            Teacher_Info.objects.get(Email=request.data['Eamil'])  
            return render (request, 'Temp_1/page-404-2.html' )
          except:
             pass
          try:
            Student_Info.objects.get(User=request.data['User'])  
            return render (request, 'Temp_1/page-404-2.html' )
          except:
             pass
          try:
            Student_Info.objects.get(Email=request.data['Eamil'])  
            return render (request, 'Temp_1/page-404-2.html' )
          except:
             pass
          serializer = Teacher_Serializer(data=request.data)
          if serializer.is_valid():
             serializer.save()
             complete = Teacher_Info.objects.last()
             rand_int =  random.randint(1,10)
             shutil.copyfile(f"{BASE_DIR}/static/Default/{rand_int}.jpg", f"{BASE_DIR}/media/Teachers/{str(complete.id)}.jpg")
             Teacher_Info.objects.filter(id= complete.id).update(School_Name = f"New School-{str(complete.id)}", School_Type= "Unknown", School_Descriptions="This is a default description for your school, update this with the related infomation.", Currency="$")
             response =  redirect('home')
            # file_text = open(f"{BASE_DIR}/Handler/Emails/Register.html", "r")
             #raw_html = file_text.read()
             #print(raw_html)
             random_uuid = uuid.uuid1()
             
             Verify.objects.create(User=complete.id,Uid=random_uuid,Type=complete.Type)

             sender_email = "dalabassistantce@gmail.com"
             receiver_email = complete.Email
             password = "fskywsbvgrytdpam"
             message = MIMEMultipart("alternative")
             message["Subject"] = "Dalab Assistance Says"
             message["From"] = sender_email
             message["To"] = receiver_email
         
# Create the plain-text and HTML version of your message
             text = """\
          Hi,
          How are you?
          You are to verify this account:
          www.dalabcloud.pythonanywhere.com"""
             html = """\
            
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" style="font-family:arial, 'helvetica neue', helvetica, sans-serif">
 <head>
  <meta charset="UTF-8">
  <meta content="width=device-width, initial-scale=1" name="viewport">
  <meta name="x-apple-disable-message-reformatting">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta content="telephone=no" name="format-detection">
  <title>New email template 2023-02-07</title><!--[if (mso 16)]>
    <style type="text/css">
    a {text-decoration: none;}
    </style>
    <![endif]--><!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]--><!--[if gte mso 9]>
<xml>
    <o:OfficeDocumentSettings>
    <o:AllowPNG></o:AllowPNG>
    <o:PixelsPerInch>96</o:PixelsPerInch>
    </o:OfficeDocumentSettings>
</xml>
<![endif]--><!--[if !mso]><!-- -->
  <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet"><!--<![endif]-->
  <style type="text/css">
#outlook a {
	padding:0;
}
.es-button {
	mso-style-priority:100!important;
	text-decoration:none!important;
}
a[x-apple-data-detectors] {
	color:inherit!important;
	text-decoration:none!important;
	font-size:inherit!important;
	font-family:inherit!important;
	font-weight:inherit!important;
	line-height:inherit!important;
}
.es-desk-hidden {
	display:none;
	float:left;
	overflow:hidden;
	width:0;
	max-height:0;
	line-height:0;
	mso-hide:all;
}
[data-ogsb] .es-button {
	border-width:0!important;
	padding:10px 40px 10px 40px!important;
}
[data-ogsb] .es-button.es-button-1 {
	padding:15px 5px!important;
}
@media only screen and (max-width:600px) {p, ul li, ol li, a { line-height:150%!important } h1, h2, h3, h1 a, h2 a, h3 a { line-height:120% } h1 { font-size:36px!important; text-align:left } h2 { font-size:28px!important; text-align:left } h3 { font-size:20px!important; text-align:left } .es-header-body h1 a, .es-content-body h1 a, .es-footer-body h1 a { font-size:36px!important; text-align:left } .es-header-body h2 a, .es-content-body h2 a, .es-footer-body h2 a { font-size:28px!important; text-align:left } .es-header-body h3 a, .es-content-body h3 a, .es-footer-body h3 a { font-size:20px!important; text-align:left } .es-menu td a { font-size:14px!important } .es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a { font-size:14px!important } .es-content-body p, .es-content-body ul li, .es-content-body ol li, .es-content-body a { font-size:14px!important } .es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a { font-size:14px!important } .es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a { font-size:12px!important } *[class="gmail-fix"] { display:none!important } .es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3 { text-align:center!important } .es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3 { text-align:right!important } .es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3 { text-align:left!important } .es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img { display:inline!important } .es-button-border { display:block!important } a.es-button, button.es-button { font-size:18px!important; display:block!important; border-right-width:0px!important; border-left-width:0px!important; border-top-width:15px!important; border-bottom-width:15px!important } .es-adaptive table, .es-left, .es-right { width:100%!important } .es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header { width:100%!important; max-width:600px!important } .es-adapt-td { display:block!important; width:100%!important } .adapt-img { width:100%!important; height:auto!important } .es-m-p0 { padding:0!important } .es-m-p0r { padding-right:0!important } .es-m-p0l { padding-left:0!important } .es-m-p0t { padding-top:0!important } .es-m-p0b { padding-bottom:0!important } .es-m-p20b { padding-bottom:20px!important } .es-mobile-hidden, .es-hidden { display:none!important } tr.es-desk-hidden, td.es-desk-hidden, table.es-desk-hidden { width:auto!important; overflow:visible!important; float:none!important; max-height:inherit!important; line-height:inherit!important } tr.es-desk-hidden { display:table-row!important } table.es-desk-hidden { display:table!important } td.es-desk-menu-hidden { display:table-cell!important } .es-menu td { width:1%!important } table.es-table-not-adapt, .esd-block-html table { width:auto!important } table.es-social { display:inline-block!important } table.es-social td { display:inline-block!important } .es-desk-hidden { display:table-row!important; width:auto!important; overflow:visible!important; max-height:inherit!important } .es-m-p5 { padding:5px!important } .es-m-p5t { padding-top:5px!important } .es-m-p5b { padding-bottom:5px!important } .es-m-p5r { padding-right:5px!important } .es-m-p5l { padding-left:5px!important } .es-m-p10 { padding:10px!important } .es-m-p10t { padding-top:10px!important } .es-m-p10b { padding-bottom:10px!important } .es-m-p10r { padding-right:10px!important } .es-m-p10l { padding-left:10px!important } .es-m-p15 { padding:15px!important } .es-m-p15t { padding-top:15px!important } .es-m-p15b { padding-bottom:15px!important } .es-m-p15r { padding-right:15px!important } .es-m-p15l { padding-left:15px!important } .es-m-p20 { padding:20px!important } .es-m-p20t { padding-top:20px!important } .es-m-p20r { padding-right:20px!important } .es-m-p20l { padding-left:20px!important } .es-m-p25 { padding:25px!important } .es-m-p25t { padding-top:25px!important } .es-m-p25b { padding-bottom:25px!important } .es-m-p25r { padding-right:25px!important } .es-m-p25l { padding-left:25px!important } .es-m-p30 { padding:30px!important } .es-m-p30t { padding-top:30px!important } .es-m-p30b { padding-bottom:30px!important } .es-m-p30r { padding-right:30px!important } .es-m-p30l { padding-left:30px!important } .es-m-p35 { padding:35px!important } .es-m-p35t { padding-top:35px!important } .es-m-p35b { padding-bottom:35px!important } .es-m-p35r { padding-right:35px!important } .es-m-p35l { padding-left:35px!important } .es-m-p40 { padding:40px!important } .es-m-p40t { padding-top:40px!important } .es-m-p40b { padding-bottom:40px!important } .es-m-p40r { padding-right:40px!important } .es-m-p40l { padding-left:40px!important } }
</style>
 </head>
 <body style="width:100%;font-family:arial, 'helvetica neue', helvetica, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">
  <div class="es-wrapper-color" style="background-color:#F9F4FF"><!--[if gte mso 9]>
			<v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
				<v:fill type="tile" src="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/rectangle_171_3.png" color="#F9F4FF" origin="0.5, 0" position="0.5, 0"></v:fill>
			</v:background>
		<![endif]-->
   <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" background="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/rectangle_171_3.png" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-image:url(https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/rectangle_171_3.png);background-repeat:repeat;background-position:center top;background-color:#F9F4FF">
     <tr>
      <td valign="top" style="padding:0;Margin:0">
       <table cellpadding="0" cellspacing="0" class="es-header" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-header-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr>
              <td align="left" style="Margin:0;padding-top:20px;padding-left:20px;padding-right:20px;padding-bottom:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:560px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;font-size:0px"><a target="_blank" href="https://dalabcloud.pythonanywhere.com/Manager" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#666666;font-size:14px"><img src="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/group.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="40"></a></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#1B1B1B;width:600px">
             <tr>
              <td align="left" style="Margin:0;padding-top:30px;padding-bottom:30px;padding-left:40px;padding-right:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="center" valign="top" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;font-size:0px"><a target="_blank" href="https://dalabcloud.pythonanywhere.com/Manager" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#E9E9E9;font-size:16px"><img src="https://gcejva.stripocdn.email/content/guids/CABINET_9aa36f49cdb5185ad35ee0f7a5c7d9380ade3ae69ada3493ecaa145d1284bee9/images/25469811_developer_male_ICK.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="280" class="adapt-img"></a></td>
                     </tr>
                     <tr>
                      <td align="center" class="es-m-txt-c" style="padding:0;Margin:0;padding-top:20px;padding-bottom:20px"><h1 style="Margin:0;line-height:60px;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;font-size:40px;font-style:normal;font-weight:bold;color:#E9E9E9">DalabCloud Assistance</h1></td>
                     </tr>
                   </table></td>
                 </tr>
                 <tr>
                  <td align="center" valign="top" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:separate;border-spacing:0px;border-width:2px;border-style:solid;border-color:#4ca2f8;border-radius:20px;background-image:url(https://gcejva.stripocdn.email/content/guids/CABINET_9aa36f49cdb5185ad35ee0f7a5c7d9380ade3ae69ada3493ecaa145d1284bee9/images/group_347_1.png);background-repeat:no-repeat;background-position:left center" background="https://gcejva.stripocdn.email/content/guids/CABINET_9aa36f49cdb5185ad35ee0f7a5c7d9380ade3ae69ada3493ecaa145d1284bee9/images/group_347_1.png" role="presentation">
                     <tr>
                      <td align="left" class="es-m-p20r es-m-p20l" style="padding:40px;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;line-height:24px;color:#E9E9E9;font-size:16px">Hi <strong>"""+complete.Full_Name+"""</strong>,<br><br>Click on the button bellow to verify your account!<br>Thank you for using DalabCloud.<br></p><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;line-height:24px;color:#ff0000;font-size:16px;text-align:center"><span style="font-size:22px"></span>&nbsp;</p></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
             <tr>
              <td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:40px;padding-right:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="center" valign="top" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;padding-bottom:20px"><!--[if mso]><a href="https://dalabcloud.pythonanywhere.com/Manager" target="_blank" hidden>
	<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" esdevVmlButton href="https://dalabcloud.pythonanywhere.com/Manager" 
                style="height:51px; v-text-anchor:middle; width:520px" arcsize="50%" stroke="f"  fillcolor="#4ca2f8">
		<w:anchorlock></w:anchorlock>
		<center style='color:#ffffff; font-family:Poppins, sans-serif; font-size:18px; font-weight:400; line-height:18px;  mso-text-raise:1px'>Goto Login</center>
	</v:roundrect></a>
<![endif]--><!--[if !mso]><!-- --><span class="msohide es-button-border" style="border-style:solid;border-color:#2CB543;background:#4CA2F8;border-width:0px;display:block;border-radius:30px;width:auto;mso-hide:all"><a href='http://127.0.0.1:2000/notify/"""+str(random_uuid)+""" ' class="es-button msohide es-button-1" target="_blank" style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;color:#FFFFFF;font-size:18px;border-style:solid;border-color:#4CA2F8;border-width:15px 5px;display:block;background:#4CA2F8;border-radius:30px;font-family:Poppins, sans-serif;font-weight:normal;font-style:normal;line-height:22px;width:auto;text-align:center;mso-hide:all">Verify This Account!</a></span><!--<![endif]--></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#1B1B1B;width:600px">
             <tr>
              <td align="left" background="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/20347363_v1072014converted_1_GkL.png" style="padding:0;Margin:0;padding-top:20px;padding-left:40px;padding-right:40px;background-image:url(https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/20347363_v1072014converted_1_GkL.png);background-repeat:no-repeat;background-position:right top">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="center" valign="top" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="left" class="es-m-p0r es-m-p0l" style="padding:0;Margin:0;padding-top:20px;padding-left:40px;padding-right:40px"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;line-height:24px;color:#E9E9E9;font-size:16px">Thanks,<br><strong>Dalabcloud Assistance</strong></p></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
             <tr>
              <td class="es-m-p40l" align="left" style="padding:0;Margin:0;padding-left:20px;padding-bottom:40px;padding-right:40px"><!--[if mso]><table style="width:540px" cellpadding="0" cellspacing="0"><tr><td style="width:46px" valign="top"><![endif]-->
               <table cellpadding="0" cellspacing="0" class="es-left" align="left" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">
                 <tr class="es-mobile-hidden">
                  <td class="es-m-p20b" align="left" style="padding:0;Margin:0;width:46px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" height="40" style="padding:0;Margin:0"></td>
                     </tr>
                   </table></td>
                 </tr>
               </table><!--[if mso]></td><td style="width:10px"></td><td style="width:484px" valign="top"><![endif]-->
               <table cellpadding="0" cellspacing="0" class="es-right" align="right" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:484px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td style="padding:0;Margin:0">
                       <table cellpadding="0" cellspacing="0" width="100%" class="es-menu" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                         <tr class="links-images-left">
                          <td align="left" valign="top" width="100%" style="padding:0;Margin:0;padding-right:5px;padding-top:10px;padding-bottom:5px;border:0" id="esd-menu-id-0"><a target="_blank" href="tel:+(000)123456789" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:none;display:block;font-family:Poppins, sans-serif;color:#E9E9E9;font-size:16px"><img src="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/envelope_1.png" alt="+ (253) 771 465 09" title="+ (253) 771 465 09" align="absmiddle" width="20" style="display:inline-block !important;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;padding-right:15px;vertical-align:middle">+ (253) 771 465 09</a></td>
                         </tr>
                       </table></td>
                     </tr>
                     <tr>
                      <td style="padding:0;Margin:0">
                       <table cellpadding="0" cellspacing="0" width="100%" class="es-menu" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                         <tr class="links-images-left">
                          <td align="left" valign="top" width="100%" style="padding:0;Margin:0;padding-right:5px;padding-top:0px;padding-bottom:5px;border:0" id="esd-menu-id-0"><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:none;display:block;font-family:Poppins, sans-serif;color:#E9E9E9;font-size:16px"><img src="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/envelope.png" alt="dalab@email.com" title="dalab@email.com" align="absmiddle" width="20" style="display:inline-block !important;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;padding-right:15px;vertical-align:middle">dalab@email.com</a></td>
                         </tr>
                       </table></td>
                     </tr>
                   </table></td>
                 </tr>
               </table><!--[if mso]></td></tr></table><![endif]--></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-footer" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-footer-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr>
              <td align="left" bgcolor="#77c82a" style="Margin:0;padding-top:20px;padding-bottom:20px;padding-left:20px;padding-right:20px;background-color:#77c82a">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:560px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;font-size:0">
                       <table cellpadding="0" cellspacing="0" class="es-table-not-adapt es-social" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                         <tr>
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="https://viewstripo.email" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Facebook" src="https://gcejva.stripocdn.email/content/assets/img/social-icons/circle-white/facebook-circle-white.png" alt="Fb" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="https://viewstripo.email" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Twitter" src="https://gcejva.stripocdn.email/content/assets/img/social-icons/circle-white/twitter-circle-white.png" alt="Tw" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="https://viewstripo.email" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Instagram" src="https://gcejva.stripocdn.email/content/assets/img/social-icons/circle-white/instagram-circle-white.png" alt="Inst" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                          <td align="center" valign="top" style="padding:0;Margin:0"><a target="_blank" href="https://viewstripo.email" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Youtube" src="https://gcejva.stripocdn.email/content/assets/img/social-icons/circle-white/youtube-circle-white.png" alt="Yt" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                         </tr>
                       </table></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-footer" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table class="es-footer-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px" bgcolor="#FFFFFF">
             <tr>
              <td align="left" style="Margin:0;padding-top:20px;padding-bottom:20px;padding-left:40px;padding-right:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;display:none"></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-footer" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-footer-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr>
              <td align="left" style="Margin:0;padding-top:20px;padding-bottom:20px;padding-left:40px;padding-right:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;display:none"></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table></td>
     </tr>
   </table>
  </div>
 </body>
</html>


          """
             part1 = MIMEText(text, "plain")
             part2 = MIMEText(html, "html")
             message.attach(part1)
             message.attach(part2)
             context = ssl.create_default_context()
             with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
              server.login(sender_email, password)
              server.sendmail(
              sender_email, receiver_email, message.as_string()
              ) 
             try:
               look_up = Cookie_Handler.objects.get(User=complete.id, Type="Teacher")
               generated_uuid = look_up.Cookie
             except:
               generated_uuid = uuid.uuid1()
               Cookie_Handler.objects.create(User=complete.id,Cookie = generated_uuid,Type="Teacher")
             response.set_cookie('csrf-session-xdii-token',generated_uuid)
             return response 
          else:
             
            return render (request, 'Temp_1/page-404.html' )
        else:
           try:
            Teacher_Info.objects.get(User=request.data['User'])  
            return render (request, 'Temp_1/page-404-2.html' )
           except:
             pass
           try:
            Teacher_Info.objects.get(Email=request.data['Eamil'])  
            return render (request, 'Temp_1/page-404-2.html' )
           except:
             pass
           try:
            Student_Info.objects.get(User=request.data['User'])  
            return render (request, 'Temp_1/page-404-2.html' )
           except:
             pass
           try:
            Student_Info.objects.get(Email=request.data['Eamil'])  
            return render (request, 'Temp_1/page-404-2.html' )
           except:
             pass
           serializer = Student_Serializer(data=request.data)
           if serializer.is_valid():
             serializer.save()
             data = Student_Info.objects.last()
             rand_int =  random.randint(1,10)
             shutil.copyfile(f"{BASE_DIR}/static/Default/users/{rand_int}.jpg", f"{BASE_DIR}/media/Students/{str(data.id)}.jpg")
             response =  redirect('home')
             random_uuid = uuid.uuid1()
             Verify.objects.create(User=data.id,Uid=random_uuid,Type=data.Type)

             sender_email = "dalabassistantce@gmail.com"
             receiver_email = data.Email
             password = "fskywsbvgrytdpam"
             message = MIMEMultipart("alternative")
             message["Subject"] = "Dalab Assistance Says"
             message["From"] = sender_email
             message["To"] = receiver_email
         
# Create the plain-text and HTML version of your message
             text = """\
          Hi,
          How are you?
          You are to verify this account:
          www.dalabcloud.pythonanywhere.com"""
             html = """\
            
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" style="font-family:arial, 'helvetica neue', helvetica, sans-serif">
 <head>
  <meta charset="UTF-8">
  <meta content="width=device-width, initial-scale=1" name="viewport">
  <meta name="x-apple-disable-message-reformatting">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta content="telephone=no" name="format-detection">
  <title>New email template 2023-02-07</title><!--[if (mso 16)]>
    <style type="text/css">
    a {text-decoration: none;}
    </style>
    <![endif]--><!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]--><!--[if gte mso 9]>
<xml>
    <o:OfficeDocumentSettings>
    <o:AllowPNG></o:AllowPNG>
    <o:PixelsPerInch>96</o:PixelsPerInch>
    </o:OfficeDocumentSettings>
</xml>
<![endif]--><!--[if !mso]><!-- -->
  <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet"><!--<![endif]-->
  <style type="text/css">
#outlook a {
	padding:0;
}
.es-button {
	mso-style-priority:100!important;
	text-decoration:none!important;
}
a[x-apple-data-detectors] {
	color:inherit!important;
	text-decoration:none!important;
	font-size:inherit!important;
	font-family:inherit!important;
	font-weight:inherit!important;
	line-height:inherit!important;
}
.es-desk-hidden {
	display:none;
	float:left;
	overflow:hidden;
	width:0;
	max-height:0;
	line-height:0;
	mso-hide:all;
}
[data-ogsb] .es-button {
	border-width:0!important;
	padding:10px 40px 10px 40px!important;
}
[data-ogsb] .es-button.es-button-1 {
	padding:15px 5px!important;
}
@media only screen and (max-width:600px) {p, ul li, ol li, a { line-height:150%!important } h1, h2, h3, h1 a, h2 a, h3 a { line-height:120% } h1 { font-size:36px!important; text-align:left } h2 { font-size:28px!important; text-align:left } h3 { font-size:20px!important; text-align:left } .es-header-body h1 a, .es-content-body h1 a, .es-footer-body h1 a { font-size:36px!important; text-align:left } .es-header-body h2 a, .es-content-body h2 a, .es-footer-body h2 a { font-size:28px!important; text-align:left } .es-header-body h3 a, .es-content-body h3 a, .es-footer-body h3 a { font-size:20px!important; text-align:left } .es-menu td a { font-size:14px!important } .es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a { font-size:14px!important } .es-content-body p, .es-content-body ul li, .es-content-body ol li, .es-content-body a { font-size:14px!important } .es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a { font-size:14px!important } .es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a { font-size:12px!important } *[class="gmail-fix"] { display:none!important } .es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3 { text-align:center!important } .es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3 { text-align:right!important } .es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3 { text-align:left!important } .es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img { display:inline!important } .es-button-border { display:block!important } a.es-button, button.es-button { font-size:18px!important; display:block!important; border-right-width:0px!important; border-left-width:0px!important; border-top-width:15px!important; border-bottom-width:15px!important } .es-adaptive table, .es-left, .es-right { width:100%!important } .es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header { width:100%!important; max-width:600px!important } .es-adapt-td { display:block!important; width:100%!important } .adapt-img { width:100%!important; height:auto!important } .es-m-p0 { padding:0!important } .es-m-p0r { padding-right:0!important } .es-m-p0l { padding-left:0!important } .es-m-p0t { padding-top:0!important } .es-m-p0b { padding-bottom:0!important } .es-m-p20b { padding-bottom:20px!important } .es-mobile-hidden, .es-hidden { display:none!important } tr.es-desk-hidden, td.es-desk-hidden, table.es-desk-hidden { width:auto!important; overflow:visible!important; float:none!important; max-height:inherit!important; line-height:inherit!important } tr.es-desk-hidden { display:table-row!important } table.es-desk-hidden { display:table!important } td.es-desk-menu-hidden { display:table-cell!important } .es-menu td { width:1%!important } table.es-table-not-adapt, .esd-block-html table { width:auto!important } table.es-social { display:inline-block!important } table.es-social td { display:inline-block!important } .es-desk-hidden { display:table-row!important; width:auto!important; overflow:visible!important; max-height:inherit!important } .es-m-p5 { padding:5px!important } .es-m-p5t { padding-top:5px!important } .es-m-p5b { padding-bottom:5px!important } .es-m-p5r { padding-right:5px!important } .es-m-p5l { padding-left:5px!important } .es-m-p10 { padding:10px!important } .es-m-p10t { padding-top:10px!important } .es-m-p10b { padding-bottom:10px!important } .es-m-p10r { padding-right:10px!important } .es-m-p10l { padding-left:10px!important } .es-m-p15 { padding:15px!important } .es-m-p15t { padding-top:15px!important } .es-m-p15b { padding-bottom:15px!important } .es-m-p15r { padding-right:15px!important } .es-m-p15l { padding-left:15px!important } .es-m-p20 { padding:20px!important } .es-m-p20t { padding-top:20px!important } .es-m-p20r { padding-right:20px!important } .es-m-p20l { padding-left:20px!important } .es-m-p25 { padding:25px!important } .es-m-p25t { padding-top:25px!important } .es-m-p25b { padding-bottom:25px!important } .es-m-p25r { padding-right:25px!important } .es-m-p25l { padding-left:25px!important } .es-m-p30 { padding:30px!important } .es-m-p30t { padding-top:30px!important } .es-m-p30b { padding-bottom:30px!important } .es-m-p30r { padding-right:30px!important } .es-m-p30l { padding-left:30px!important } .es-m-p35 { padding:35px!important } .es-m-p35t { padding-top:35px!important } .es-m-p35b { padding-bottom:35px!important } .es-m-p35r { padding-right:35px!important } .es-m-p35l { padding-left:35px!important } .es-m-p40 { padding:40px!important } .es-m-p40t { padding-top:40px!important } .es-m-p40b { padding-bottom:40px!important } .es-m-p40r { padding-right:40px!important } .es-m-p40l { padding-left:40px!important } }
</style>
 </head>
 <body style="width:100%;font-family:arial, 'helvetica neue', helvetica, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">
  <div class="es-wrapper-color" style="background-color:#F9F4FF"><!--[if gte mso 9]>
			<v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
				<v:fill type="tile" src="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/rectangle_171_3.png" color="#F9F4FF" origin="0.5, 0" position="0.5, 0"></v:fill>
			</v:background>
		<![endif]-->
   <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" background="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/rectangle_171_3.png" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-image:url(https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/rectangle_171_3.png);background-repeat:repeat;background-position:center top;background-color:#F9F4FF">
     <tr>
      <td valign="top" style="padding:0;Margin:0">
       <table cellpadding="0" cellspacing="0" class="es-header" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-header-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr>
              <td align="left" style="Margin:0;padding-top:20px;padding-left:20px;padding-right:20px;padding-bottom:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:560px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;font-size:0px"><a target="_blank" href="https://dalabcloud.pythonanywhere.com/Manager" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#666666;font-size:14px"><img src="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/group.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="40"></a></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#1B1B1B;width:600px">
             <tr>
              <td align="left" style="Margin:0;padding-top:30px;padding-bottom:30px;padding-left:40px;padding-right:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="center" valign="top" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;font-size:0px"><a target="_blank" href="https://dalabcloud.pythonanywhere.com/Manager" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#E9E9E9;font-size:16px"><img src="https://gcejva.stripocdn.email/content/guids/CABINET_9aa36f49cdb5185ad35ee0f7a5c7d9380ade3ae69ada3493ecaa145d1284bee9/images/25469811_developer_male_ICK.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="280" class="adapt-img"></a></td>
                     </tr>
                     <tr>
                      <td align="center" class="es-m-txt-c" style="padding:0;Margin:0;padding-top:20px;padding-bottom:20px"><h1 style="Margin:0;line-height:60px;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;font-size:40px;font-style:normal;font-weight:bold;color:#E9E9E9">DalabCloud Assistance</h1></td>
                     </tr>
                   </table></td>
                 </tr>
                 <tr>
                  <td align="center" valign="top" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:separate;border-spacing:0px;border-width:2px;border-style:solid;border-color:#4ca2f8;border-radius:20px;background-image:url(https://gcejva.stripocdn.email/content/guids/CABINET_9aa36f49cdb5185ad35ee0f7a5c7d9380ade3ae69ada3493ecaa145d1284bee9/images/group_347_1.png);background-repeat:no-repeat;background-position:left center" background="https://gcejva.stripocdn.email/content/guids/CABINET_9aa36f49cdb5185ad35ee0f7a5c7d9380ade3ae69ada3493ecaa145d1284bee9/images/group_347_1.png" role="presentation">
                     <tr>
                      <td align="left" class="es-m-p20r es-m-p20l" style="padding:40px;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;line-height:24px;color:#E9E9E9;font-size:16px">Hi <strong>"""+data.Full_Name+"""</strong>,<br><br>Click on the button bellow to verify your account!<br>Thank you for using DalabCloud.<br></p><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;line-height:24px;color:#ff0000;font-size:16px;text-align:center"><span style="font-size:22px"></span>&nbsp;</p></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
             <tr>
              <td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:40px;padding-right:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="center" valign="top" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;padding-bottom:20px"><!--[if mso]><a href="https://dalabcloud.pythonanywhere.com/Manager" target="_blank" hidden>
	<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" esdevVmlButton href="https://dalabcloud.pythonanywhere.com/Manager" 
                style="height:51px; v-text-anchor:middle; width:520px" arcsize="50%" stroke="f"  fillcolor="#4ca2f8">
		<w:anchorlock></w:anchorlock>
		<center style='color:#ffffff; font-family:Poppins, sans-serif; font-size:18px; font-weight:400; line-height:18px;  mso-text-raise:1px'>Goto Login</center>
	</v:roundrect></a>
<![endif]--><!--[if !mso]><!-- --><span class="msohide es-button-border" style="border-style:solid;border-color:#2CB543;background:#4CA2F8;border-width:0px;display:block;border-radius:30px;width:auto;mso-hide:all"><a href='http://127.0.0.1:2000/notify/"""+str(random_uuid)+""" ' class="es-button msohide es-button-1" target="_blank" style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;color:#FFFFFF;font-size:18px;border-style:solid;border-color:#4CA2F8;border-width:15px 5px;display:block;background:#4CA2F8;border-radius:30px;font-family:Poppins, sans-serif;font-weight:normal;font-style:normal;line-height:22px;width:auto;text-align:center;mso-hide:all">Verify This Account!</a></span><!--<![endif]--></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#1B1B1B;width:600px">
             <tr>
              <td align="left" background="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/20347363_v1072014converted_1_GkL.png" style="padding:0;Margin:0;padding-top:20px;padding-left:40px;padding-right:40px;background-image:url(https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/20347363_v1072014converted_1_GkL.png);background-repeat:no-repeat;background-position:right top">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="center" valign="top" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="left" class="es-m-p0r es-m-p0l" style="padding:0;Margin:0;padding-top:20px;padding-left:40px;padding-right:40px"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;line-height:24px;color:#E9E9E9;font-size:16px">Thanks,<br><strong>Dalabcloud Assistance</strong></p></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
             <tr>
              <td class="es-m-p40l" align="left" style="padding:0;Margin:0;padding-left:20px;padding-bottom:40px;padding-right:40px"><!--[if mso]><table style="width:540px" cellpadding="0" cellspacing="0"><tr><td style="width:46px" valign="top"><![endif]-->
               <table cellpadding="0" cellspacing="0" class="es-left" align="left" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">
                 <tr class="es-mobile-hidden">
                  <td class="es-m-p20b" align="left" style="padding:0;Margin:0;width:46px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" height="40" style="padding:0;Margin:0"></td>
                     </tr>
                   </table></td>
                 </tr>
               </table><!--[if mso]></td><td style="width:10px"></td><td style="width:484px" valign="top"><![endif]-->
               <table cellpadding="0" cellspacing="0" class="es-right" align="right" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:484px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td style="padding:0;Margin:0">
                       <table cellpadding="0" cellspacing="0" width="100%" class="es-menu" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                         <tr class="links-images-left">
                          <td align="left" valign="top" width="100%" style="padding:0;Margin:0;padding-right:5px;padding-top:10px;padding-bottom:5px;border:0" id="esd-menu-id-0"><a target="_blank" href="tel:+(000)123456789" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:none;display:block;font-family:Poppins, sans-serif;color:#E9E9E9;font-size:16px"><img src="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/envelope_1.png" alt="+ (253) 771 465 09" title="+ (253) 771 465 09" align="absmiddle" width="20" style="display:inline-block !important;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;padding-right:15px;vertical-align:middle">+ (253) 771 465 09</a></td>
                         </tr>
                       </table></td>
                     </tr>
                     <tr>
                      <td style="padding:0;Margin:0">
                       <table cellpadding="0" cellspacing="0" width="100%" class="es-menu" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                         <tr class="links-images-left">
                          <td align="left" valign="top" width="100%" style="padding:0;Margin:0;padding-right:5px;padding-top:0px;padding-bottom:5px;border:0" id="esd-menu-id-0"><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:none;display:block;font-family:Poppins, sans-serif;color:#E9E9E9;font-size:16px"><img src="https://gcejva.stripocdn.email/content/guids/CABINET_b5bfed0b11252243ebfb1c00df0e3977/images/envelope.png" alt="dalab@email.com" title="dalab@email.com" align="absmiddle" width="20" style="display:inline-block !important;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;padding-right:15px;vertical-align:middle">dalab@email.com</a></td>
                         </tr>
                       </table></td>
                     </tr>
                   </table></td>
                 </tr>
               </table><!--[if mso]></td></tr></table><![endif]--></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-footer" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-footer-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr>
              <td align="left" bgcolor="#77c82a" style="Margin:0;padding-top:20px;padding-bottom:20px;padding-left:20px;padding-right:20px;background-color:#77c82a">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:560px">
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;font-size:0">
                       <table cellpadding="0" cellspacing="0" class="es-table-not-adapt es-social" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                         <tr>
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="https://viewstripo.email" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Facebook" src="https://gcejva.stripocdn.email/content/assets/img/social-icons/circle-white/facebook-circle-white.png" alt="Fb" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="https://viewstripo.email" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Twitter" src="https://gcejva.stripocdn.email/content/assets/img/social-icons/circle-white/twitter-circle-white.png" alt="Tw" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="https://viewstripo.email" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Instagram" src="https://gcejva.stripocdn.email/content/assets/img/social-icons/circle-white/instagram-circle-white.png" alt="Inst" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                          <td align="center" valign="top" style="padding:0;Margin:0"><a target="_blank" href="https://viewstripo.email" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Youtube" src="https://gcejva.stripocdn.email/content/assets/img/social-icons/circle-white/youtube-circle-white.png" alt="Yt" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                         </tr>
                       </table></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-footer" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table class="es-footer-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px" bgcolor="#FFFFFF">
             <tr>
              <td align="left" style="Margin:0;padding-top:20px;padding-bottom:20px;padding-left:40px;padding-right:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;display:none"></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table>
       <table cellpadding="0" cellspacing="0" class="es-footer" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
         <tr>
          <td align="center" style="padding:0;Margin:0">
           <table bgcolor="#ffffff" class="es-footer-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
             <tr>
              <td align="left" style="Margin:0;padding-top:20px;padding-bottom:20px;padding-left:40px;padding-right:40px">
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                 <tr>
                  <td align="left" style="padding:0;Margin:0;width:520px">
                   <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                     <tr>
                      <td align="center" style="padding:0;Margin:0;display:none"></td>
                     </tr>
                   </table></td>
                 </tr>
               </table></td>
             </tr>
           </table></td>
         </tr>
       </table></td>
     </tr>
   </table>
  </div>
 </body>
</html>


          """
             part1 = MIMEText(text, "plain")
             part2 = MIMEText(html, "html")
             message.attach(part1)
             message.attach(part2)
             context = ssl.create_default_context()
             with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
              server.login(sender_email, password)
              server.sendmail(
              sender_email, receiver_email, message.as_string()
              ) 
             try:
               look_up = Cookie_Handler.objects.get(User=data.id, Type="Student")
               generated_uuid = look_up.Cookie
             except:
               generated_uuid = uuid.uuid1()
               Cookie_Handler.objects.create(User=data.id,Cookie = generated_uuid,Type="Student")
             response.set_cookie('csrf-session-xdii-token',generated_uuid)
             return response 
           else:
             return render (request, 'Temp_1/page-404.html' )
     

class Logout(APIView):
    def get(self , request):
      response = redirect("login")
      response.delete_cookie('csrf-session-xdii-token')

      return response

#===================================================== Login / Register / Logout =======================================


#===================================================== Notifications =====================================================
class Notify(APIView):
    def get(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          notified = []
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          if find.Type == "Teacher":
           User_data = Teacher_Info.objects.get(id=int(find.User))
           listed = Notifications.objects.filter(Uid=User_data.id,Type="Teacher",Status="New").all()
           for i in listed:
             notified.append({
               "id":i.id,"Info":i.Info,"date":i.date,
             })
             Notifications.objects.filter(id = i.id).update(Status="Old")
          else:
           User_data = Student_Info.objects.get(id=int(find.User))
           listed = Notifications.objects.filter(Uid=User_data.id,Type="Student",Status="New").all()
           
           for i in listed:
             notified.append({
               "id":i.id,"Info":i.Info,"date":i.date,
             })
             Notifications.objects.filter(id = i.id).update(Status="Old")
          print(listed)   
          return Response(notified)
         except:
           return Response("Login")
      return Response("Login")
    
#===================================================== Notifications =====================================================


#==================================================== Verify ===========================================================
class Verify_Page(APIView):
    def get(self , request,pk):
     try:
      verify = Verify.objects.get(Uid=pk)
      if verify.Type == "Teacher":
        Teacher_Info.objects.filter(id=int(verify.User)).update(Verify="Yes")
      else:
        Student_Info.objects.filter(id=int(verify.User)).update(Verify="Yes")  
      return redirect('home')
     except:
       return render (request, 'Temp_1/page-404-2.html' )
    

#==================================================== Verify ===========================================================
