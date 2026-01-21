from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Habit(models.Model):
    CATEGORY_CHOICES = [
        ('health', 'Health'),
        ('work', 'Work'),
        ('learning', 'Learning'),
        ('personal', 'Personal'),
        ('fitness', 'Fitness'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def get_current_streak(self):
        """Calculate current streak of consecutive days"""
        completions = self.habitcompletion_set.filter(
            completed=True
        ).order_by('-date')
        
        if not completions.exists():
            return 0
        
        streak = 0
        current_date = timezone.now().date()
        
        for completion in completions:
            if completion.date == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        
        return streak
    
    def get_total_completions(self):
        """Get total number of times this habit was completed"""
        return self.habitcompletion_set.filter(completed=True).count()
    
    def is_completed_today(self):
        """Check if habit was completed today"""
        today = timezone.now().date()
        return self.habitcompletion_set.filter(
            date=today,
            completed=True
        ).exists()
    
    class Meta:
        ordering = ['-created_at']


class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.habit.name} - {self.date}"
    
    class Meta:
        unique_together = ['habit', 'date']
        ordering = ['-date']