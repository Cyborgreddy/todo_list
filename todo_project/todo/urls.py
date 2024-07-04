from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('edit/<int:pk>/', views.edit_task, name='edit_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('complete/<int:pk>/', views.complete_task, name='complete_task'),
    path('add/', views.add_task, name='add_task'),
]
