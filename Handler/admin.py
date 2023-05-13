from django.contrib import admin
from . models import Student_Info,Teacher_Info,Cookie_Handler,Module_Info,Course_Info,Topic_Info,Topic_Link,Topic_Question,Video_Link,Student_Courses,Test_Taken,Student_Result,Notifications,Admin_Info


admin.site.register(Student_Info)
admin.site.register(Teacher_Info)
admin.site.register(Cookie_Handler)
admin.site.register(Course_Info)
admin.site.register(Topic_Question)
admin.site.register(Topic_Link)
admin.site.register(Topic_Info)
admin.site.register(Video_Link)
admin.site.register(Student_Courses)
admin.site.register(Test_Taken)
admin.site.register(Student_Result)
admin.site.register(Notifications)
admin.site.register(Admin_Info)

admin.site.register(Module_Info)






