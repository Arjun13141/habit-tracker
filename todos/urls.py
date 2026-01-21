from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo-list'),
    path('create/', views.todo_create, name='todo-create'),
    path('<int:pk>/update/', views.todo_update, name='todo-update'),
    path('<int:pk>/delete/', views.todo_delete, name='todo-delete'),
    path('<int:pk>/toggle/', views.todo_toggle, name='todo-toggle'),
]