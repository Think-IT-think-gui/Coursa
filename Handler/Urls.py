from django.urls import path
from . views import Landing,Login,Register,Logout,Courses_Page,Courses_Content,Notify,Notify,Verify_Page,Courses_Get,Courses_Find
from . dashboard import Main_Dashboard
from . teachers import Create_Course,Create_Module,Module_Page,Create_Topic,Topic_Config,Course_Update,Add_Link,Add_Question,Add_Topic,Delete_Request,List_Students,Edith_Course
from . students import Bought_Courses_Content,Learn_Courses,Results_View,Results,Take_Test,Buy
from . Admin_Page import Login_Admin,Admin_Dashboard,Dashboard_Admin,Logout_Admin,Table_Admin,Table_Admin,Calendar_Admin,User_Account,Logout_Admin,Accept,Delete,View_User,User_info,View_Student,Student_info,Course_info,View_Course,Course_Cover,Delete_Course

Login
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', Landing.as_view(),name="home"),
    path('login', Login.as_view(),name="login"),
    path('register', Register.as_view(),name="register"),
    path('logout', Logout.as_view(),name="logout"),
    path('dashboard', Main_Dashboard.as_view(),name="teacher_dashboard"),
    path('create_course', Create_Course.as_view(),name="create_course"),
    path('course_update/<str:pk>', Course_Update.as_view(),name="course_update"),
    path('create_topic/<str:pk>', Create_Topic.as_view(),name="create_topic"),
    path('add_topic', Add_Topic.as_view(),name="add_topic"),
    path('add_question', Add_Question.as_view(),name="add_question"),
    path('add_link', Add_Link.as_view(),name="add_link"),
    path('delete_request', Delete_Request.as_view(),name="delete_request"),
    path('topic_config', Topic_Config.as_view(),name="topic_config"),
    path('courses_page', Courses_Page.as_view(),name="courses_page"),
    path('courses_get/<str:pk>', Courses_Get.as_view(),name="courses_get"),
    path('courses_find', Courses_Find.as_view(),name="courses_find"),


    
    path('courses_content', Courses_Content.as_view(),name="courses_content"),
    path('bought_courses_content', Bought_Courses_Content.as_view(),name="bought_courses_content"),
    path('learn_courses', Learn_Courses.as_view(),name="learn_courses"),
    path('take_test', Take_Test.as_view(),name="take_test"),
    path('results_view', Results_View.as_view(),name="results_view"),
    path('results', Results.as_view(),name="results"),
    path('list_students', List_Students.as_view(),name="list_students"),
    path('notify', Notify.as_view(),name="notify"),
    path('buy', Buy.as_view(),name="buy"),
    path('verify/<str:pk>', Verify_Page.as_view(),name="verify"),
    path('admin_login', Login_Admin.as_view(),name="admin_login"),
    path('admin_dashboard', Admin_Dashboard.as_view(),name="admin_dashboard"),
    path('admin_main', Dashboard_Admin.as_view(),name="admin_main"),
    path('logout_admin', Logout_Admin.as_view(),name="logout_admin"),
    path('chart2_admin', Calendar_Admin.as_view(),name="chart2_admin"),
    path('table_admin', Table_Admin.as_view(),name="table_admin"),
    path('accept_admin', Accept.as_view(),name="accept_admin"),
    path('delete_admin', Delete.as_view(),name="delete_admin"),
    path('module_page/<str:pk>', Module_Page.as_view(),name="module_page"),
    path('create_module', Create_Module.as_view(),name="create_module"),
    path('edith_course/<int:pk>', Edith_Course.as_view(),name="edith_course"),
    path('view_user/<int:pk>', View_User.as_view(),name="view_user"),
    path('user_info', User_info.as_view(),name="user_info"),
    path('view_student/<int:pk>', View_Student.as_view(),name="view_student"),
    path('student_info', Student_info.as_view(),name="student_info"),
    path('view_courses/<int:pk>', View_Course.as_view(),name="view_courses"),
    path('course_info', Course_info.as_view(),name="course_info"),
    path('course_cover', Course_Cover.as_view(),name="course_cover"),
    path('delete_course', Delete_Course.as_view(),name="delete_course"),



























    







    



 




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)