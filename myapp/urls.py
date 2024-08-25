from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('task/<int:id>/', views.task_detail, name='task_detail'),
    path('task/add/', views.add_task, name='add_task'),
    path('task/<int:id>/edit/', views.edit_task, name='edit_task'),
    path('task/<int:id>/delete/', views.delete_task, name='delete_task'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='registration'),
]