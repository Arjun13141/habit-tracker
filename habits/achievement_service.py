from .models import Achievement, Habit, HabitCompletion
from django.utils import timezone
from datetime import timedelta

def check_and_award_achievements(user):
    """Check if user has earned any new achievements"""
    newly_earned = []
    
    # First Habit Achievement
    if Habit.objects.filter(user=user).count() >= 1:
        achievement, created = Achievement.objects.get_or_create(
            user=user,
            achievement_type='first_habit'
        )
        if created:
            newly_earned.append(achievement)
    
    # Check all user's habits for streaks
    user_habits = Habit.objects.filter(user=user, is_active=True)
    
    for habit in user_habits:
        streak = habit.get_current_streak()
        
        # Streak achievements
        if streak >= 3:
            achievement, created = Achievement.objects.get_or_create(
                user=user,
                achievement_type='streak_3'
            )
            if created:
                newly_earned.append(achievement)
        
        if streak >= 7:
            achievement, created = Achievement.objects.get_or_create(
                user=user,
                achievement_type='streak_7'
            )
            if created:
                newly_earned.append(achievement)
        
        if streak >= 14:
            achievement, created = Achievement.objects.get_or_create(
                user=user,
                achievement_type='streak_14'
            )
            if created:
                newly_earned.append(achievement)
        
        if streak >= 30:
            achievement, created = Achievement.objects.get_or_create(
                user=user,
                achievement_type='streak_30'
            )
            if created:
                newly_earned.append(achievement)
        
        if streak >= 100:
            achievement, created = Achievement.objects.get_or_create(
                user=user,
                achievement_type='streak_100'
            )
            if created:
                newly_earned.append(achievement)
    
    # Total completions achievements
    total_completions = HabitCompletion.objects.filter(
        habit__user=user,
        completed=True
    ).count()
    
    if total_completions >= 10:
        achievement, created = Achievement.objects.get_or_create(
            user=user,
            achievement_type='complete_10'
        )
        if created:
            newly_earned.append(achievement)
    
    if total_completions >= 50:
        achievement, created = Achievement.objects.get_or_create(
            user=user,
            achievement_type='complete_50'
        )
        if created:
            newly_earned.append(achievement)
    
    if total_completions >= 100:
        achievement, created = Achievement.objects.get_or_create(
            user=user,
            achievement_type='complete_100'
        )
        if created:
            newly_earned.append(achievement)
    
    if total_completions >= 500:
        achievement, created = Achievement.objects.get_or_create(
            user=user,
            achievement_type='complete_500'
        )
        if created:
            newly_earned.append(achievement)
    
    # Perfect Week - All habits completed for 7 consecutive days
    if check_perfect_streak(user, days=7):
        achievement, created = Achievement.objects.get_or_create(
            user=user,
            achievement_type='perfect_week'
        )
        if created:
            newly_earned.append(achievement)
    
    # Perfect Month - All habits completed for 30 consecutive days
    if check_perfect_streak(user, days=30):
        achievement, created = Achievement.objects.get_or_create(
            user=user,
            achievement_type='perfect_month'
        )
        if created:
            newly_earned.append(achievement)
    
    return newly_earned


def check_perfect_streak(user, days=7):
    """Check if user completed all habits for consecutive days"""
    habits = Habit.objects.filter(user=user, is_active=True)
    
    if not habits.exists():
        return False
    
    today = timezone.now().date()
    
    for i in range(days):
        check_date = today - timedelta(days=i)
        
        # Check if all habits were completed on this date
        for habit in habits:
            completion = HabitCompletion.objects.filter(
                habit=habit,
                date=check_date,
                completed=True
            ).exists()
            
            if not completion:
                return False
    
    return True


def get_user_points(user):
    """Calculate total points for user"""
    points = 0
    
    # Points for habits
    habits_count = Habit.objects.filter(user=user, is_active=True).count()
    points += habits_count * 10
    
    # Points for completions
    completions = HabitCompletion.objects.filter(
        habit__user=user,
        completed=True
    ).count()
    points += completions * 5
    
    # Points for achievements
    achievements = Achievement.objects.filter(user=user).count()
    points += achievements * 100
    
    # Bonus points for current streaks
    user_habits = Habit.objects.filter(user=user, is_active=True)
    for habit in user_habits:
        streak = habit.get_current_streak()
        points += streak * 2
    
    return points