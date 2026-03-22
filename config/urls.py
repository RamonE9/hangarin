from django.contrib import admin
from django.urls import path, include
from allauth.account.views import LoginView
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('tasks.urls')),
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_task, name='create_task'),
    path('signup/', views.signup, name='signup'),
]