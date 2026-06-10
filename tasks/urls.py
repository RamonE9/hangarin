from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    
    # Task Dashboard & API
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tasks/', views.task_list, name='task_list'),
    path('create/', views.create_task, name='create_task'),
    path('update/<int:pk>/', views.update_task, name='update_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('complete/<int:pk>/', views.complete_task, name='complete_task'),
    path('calendar-data/', views.calendar_data, name='calendar_data'),
    path('stats/', views.task_stats, name='task_stats'),
    
    # Projects CRUD
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/update/', views.update_project, name='update_project'),
    path('projects/<int:pk>/delete/', views.delete_project, name='delete_project'),
    
    # Subtasks API (AJAX)
    path('subtasks/create/', views.create_subtask, name='create_subtask'),
    path('subtasks/<int:pk>/toggle/', views.toggle_subtask, name='toggle_subtask'),
    path('subtasks/<int:pk>/delete/', views.delete_subtask, name='delete_subtask'),
]