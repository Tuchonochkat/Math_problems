"""base_of_tasks URL Configuration

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
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView
from problems.views import start_view, LogView, problems_view, task_view, task_edit_view, new_task_view, \
    sets_view, load_categories, syllabus_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start_view),
    path('', RedirectView.as_view(url='/problems')),
    path('login/', LogView.as_view()),
    path('logout/', LogoutView.as_view(template_name='problems/logout.html')),
    path('problems/', problems_view),
    path('task_<int:id>', task_view),
    path('task_<int:id>/edit', task_edit_view),
    path('task/new', new_task_view),
    path('ajax/load-categories/', load_categories, name='ajax_load_categories'),
    path('sets/', sets_view),
    path('sets/<int:id_syllabus>', syllabus_view),
]
