from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from dashboard import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('', dashboard_views.dashboard, name='dashboard'),
    
    # Habits URLs
    path('habits/', include('habits.urls')),
    
    # Todos URLs
    path('todos/', include('todos.urls')),
]