from django.urls import path
from . import views

urlpatterns = [
    path('', views.habit_list, name='habit-list'),
    path('create/', views.habit_create, name='habit-create'),
    path('<int:pk>/update/', views.habit_update, name='habit-update'),
    path('<int:pk>/delete/', views.habit_delete, name='habit-delete'),
    path('<int:pk>/complete/', views.habit_complete, name='habit-complete'),
]