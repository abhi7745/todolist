"""todolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

import todoapp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',todoapp.views.index,name='index_url'),

    path('login/',todoapp.views.loginpage,name='login_url'),
    path('signup/',todoapp.views.signup,name='signup_url'),
    
    path('add/',todoapp.views.add,name='add_url'),
    path('todolist/',todoapp.views.todolist,name='todolist_url'),

    path('update/<int:pk>',todoapp.views.update,name='update_url'),
    path('delete/<int:pk>',todoapp.views.delete,name='delete_url'),
    path('deleteall/<int:pk>',todoapp.views.deleteall,name='deleteall_url'),
    path('completed/<int:pk>',todoapp.views.completed,name='completed_url'),
    path('logout',todoapp.views.logoutpage,name='logout_url'),

    # # other code - otp senting to mail
    # path('reset',todoapp.views.reset,name='reset_url'),
    # path('otp',todoapp.views.otp_sender,name='otp_url'),
]
