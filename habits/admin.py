from django.contrib import admin
from .models import Habit, HabitCompletion, Achievement

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'category', 'created_at', 'is_active']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'user__username']
    
@admin.register(HabitCompletion)
class HabitCompletionAdmin(admin.ModelAdmin):
    list_display = ['habit', 'date', 'completed']
    list_filter = ['completed', 'date']
    search_fields = ['habit__name']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement_type', 'earned_date']
    list_filter = ['achievement_type', 'earned_date']
    search_fields = ['user__username']