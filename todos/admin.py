from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'priority', 'completed', 'due_date', 'created_at']
    list_filter = ['completed', 'priority', 'due_date']
    search_fields = ['title', 'description', 'user__username']
    actions = ['mark_completed', 'mark_incomplete']
    
    def mark_completed(self, request, queryset):
        queryset.update(completed=True)
    mark_completed.short_description = "Mark selected todos as completed"
    
    def mark_incomplete(self, request, queryset):
        queryset.update(completed=False)
    mark_incomplete.short_description = "Mark selected todos as incomplete"