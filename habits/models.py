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
        """Calculate current streak of consecutive days - resets if missed yesterday"""
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        # Check if completed today OR yesterday (for continuity)
        completed_today = self.habitcompletion_set.filter(
            date=today,
            completed=True
        ).exists()
        
        completed_yesterday = self.habitcompletion_set.filter(
            date=yesterday,
            completed=True
        ).exists()
        
        # If didn't complete today AND didn't complete yesterday, streak is broken
        if not completed_today and not completed_yesterday:
            return 0
        
        # Count backwards from today or yesterday
        start_date = today if completed_today else yesterday
        streak = 0
        check_date = start_date
        
        while True:
            completion = self.habitcompletion_set.filter(
                date=check_date,
                completed=True
            ).exists()
            
            if completion:
                streak += 1
                check_date -= timedelta(days=1)
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


class Achievement(models.Model):
    ACHIEVEMENT_TYPES = [
        ('first_habit', 'First Habit Created'),
        ('streak_3', '3 Day Streak'),
        ('streak_7', '7 Day Streak'),
        ('streak_14', '2 Week Streak'),
        ('streak_30', '30 Day Streak'),
        ('streak_100', '100 Day Streak'),
        ('complete_10', '10 Completions'),
        ('complete_50', '50 Completions'),
        ('complete_100', '100 Completions'),
        ('complete_500', '500 Completions'),
        ('perfect_week', 'Perfect Week'),
        ('perfect_month', 'Perfect Month'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement_type = models.CharField(max_length=50, choices=ACHIEVEMENT_TYPES)
    earned_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'achievement_type']
        ordering = ['-earned_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_achievement_type_display()}"
    
    def get_badge_icon(self):
        icons = {
            'first_habit': '🎯',
            'streak_3': '🔥',
            'streak_7': '🌟',
            'streak_14': '⭐',
            'streak_30': '💫',
            'streak_100': '👑',
            'complete_10': '🏅',
            'complete_50': '🥈',
            'complete_100': '🥇',
            'complete_500': '🏆',
            'perfect_week': '📅',
            'perfect_month': '📆',
        }
        return icons.get(self.achievement_type, '🎖️')
    
    def get_badge_color(self):
        colors = {
            'first_habit': 'bg-info',
            'streak_3': 'bg-warning',
            'streak_7': 'bg-primary',
            'streak_14': 'bg-success',
            'streak_30': 'bg-danger',
            'streak_100': 'bg-dark',
            'complete_10': 'bg-info',
            'complete_50': 'bg-primary',
            'complete_100': 'bg-success',
            'complete_500': 'bg-warning',
            'perfect_week': 'bg-primary',
            'perfect_month': 'bg-success',
        }
        return colors.get(self.achievement_type, 'bg-secondary')