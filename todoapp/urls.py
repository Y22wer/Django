from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_todo, name='add'),
    path('toggle/<int:todo_id>/', views.toggle_todo, name='toggle'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete'),
]
