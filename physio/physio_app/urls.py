"""physio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import home
from . import views


urlpatterns = [
    path('physio/home',home,name='physio_home'),
    path('physio/post_tips/',views.post_tips,name='post_tips'),
    path('physio/photo_tips/',views.photo_tips,name='photo_tips'),
    path('physio/about',views.p_about,name='physio_about'),
    path('physio/appointments',views.p_appointment,name='physio_appointments'),
    path('physio/manage_profile',views.p_manage_profile,name='physio_profile'),
    path('physio/recruitment',views.p_recruit,name='recruitment'),
    path('physio/tips_success',views.tips_success,name='tips_success'),
    path('physio/manage_success',views.manage_success,name='manage_success'),
    path('physio/photo_success',views.photo_success,name='photo_success'),

    path('', views.home_page, name='home'),
    path('about', views.about, name='about'),
    path('contact',views.contact_view, name='contact'),
    path('contact_success',views.contact_success, name='contact_success'),
    path('complaints/<int:id>', views.complaints, name='complaints'),
    path('complaint_success/<int:id>', views.complaint_success, name='complaint_success'),
    path('view_tips', views.tips_view, name='tips'),
    path('treatments', views.treatments, name='treatments'),
    path('photo_video', views.photo_video, name='photo_video'),
    path('feedbacks/<int:id>', views.feedbacks, name='feedbacks'),
    path('feedback_success<int:id>', views.feedback_success, name='feedback_success'),
    path('appointments/<int:id>', views.appointments, name='appointments'),
    path('appointment_success/<int:id>', views.appointment_success, name='appointment_success'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('login_patient', views.login_patient, name='login_patient'),
    path('login_physio', views.login_physio, name='login_physio'),
    path('physio_list', views.physio_list, name='physio_list'),
    path('physio_detail/<int:id>', views.physio_detail, name='physio_detail'),
    path('patient_register', views.patient_register, name='patient_register'),
    path('physio_register', views.physio_register, name='physio_register'),
    path('edit_success', views.edit_success, name='edit_success'),
    path('physio_register_success', views.physio_register_success, name='physio_register_success'),
    path('patient_register_success', views.patient_register_success, name='patient_register_success'),
    path('manage_profile', views.manage_profile, name='manage_profile'),
    path('base', views.base, name='base'),
    path('state_ajax',views.state_ajax,name='state_ajax'),
    path('sunday_tips',views.sunday_tips,name='sunday_tips'),
    path('checkMail',views.checkMail,name='checkMail'),
    path('physio/approve_ajax',views.approve_ajax,name='approve_ajax'),
    # path('demo_file_upload', views.demo_file_upload, name='demo_file_upload'),
]
