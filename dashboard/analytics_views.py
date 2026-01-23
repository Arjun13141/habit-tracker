from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from habits.models import Habit, HabitCompletion, Achievement
from todos.models import Todo
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
from collections import defaultdict
import json

@login_required
def analytics(request):
    user = request.user
    today = timezone.now().date()
    
    # Get date range (last 30 days)
    start_date = today - timedelta(days=29)
    
    # ===== HABIT ANALYTICS =====
    
    # Get all active habits
    habits = Habit.objects.filter(user=user, is_active=True)
    total_habits = habits.count()
    
    # Daily completion data for last 30 days
    daily_completions = []
    dates_labels = []
    
    for i in range(29, -1, -1):
        date = today - timedelta(days=i)
        dates_labels.append(date.strftime('%b %d'))
        
        completed_count = HabitCompletion.objects.filter(
            habit__user=user,
            date=date,
            completed=True
        ).count()
        
        daily_completions.append(completed_count)
    
    # Category breakdown
    category_data = {}
    for habit in habits:
        category = habit.get_category_display()
        if category not in category_data:
            category_data[category] = 0
        category_data[category] += 1
    
    # Completion rate by category
    category_completion_rates = {}
    for habit in habits:
        category = habit.get_category_display()
        total_days = 30
        completed_days = HabitCompletion.objects.filter(
            habit=habit,
            date__gte=start_date,
            date__lte=today,
            completed=True
        ).count()
        
        if category not in category_completion_rates:
            category_completion_rates[category] = {'completed': 0, 'total': 0}
        
        category_completion_rates[category]['completed'] += completed_days
        category_completion_rates[category]['total'] += total_days
    
    # Calculate percentages
    category_percentages = {}
    for category, data in category_completion_rates.items():
        if data['total'] > 0:
            category_percentages[category] = round((data['completed'] / data['total']) * 100, 1)
        else:
            category_percentages[category] = 0
    
    # Best performing habits (highest completion rate)
    best_habits = []
    for habit in habits:
        completed = HabitCompletion.objects.filter(
            habit=habit,
            date__gte=start_date,
            date__lte=today,
            completed=True
        ).count()
        
        rate = (completed / 30) * 100 if completed > 0 else 0
        
        best_habits.append({
            'name': habit.name,
            'rate': round(rate, 1),
            'streak': habit.get_current_streak(),
            'category': habit.get_category_display()
        })
    
    best_habits = sorted(best_habits, key=lambda x: x['rate'], reverse=True)[:5]
    
    # Longest streak
    longest_streak = 0
    longest_streak_habit = None
    for habit in habits:
        streak = habit.get_current_streak()
        if streak > longest_streak:
            longest_streak = streak
            longest_streak_habit = habit.name
    
    # Total completions
    total_completions = HabitCompletion.objects.filter(
        habit__user=user,
        completed=True
    ).count()
    
    # ===== TODO ANALYTICS =====
    
    total_todos = Todo.objects.filter(user=user).count()
    completed_todos = Todo.objects.filter(user=user, completed=True).count()
    pending_todos = Todo.objects.filter(user=user, completed=False).count()
    
    # Completion rate
    if total_todos > 0:
        todo_completion_rate = round((completed_todos / total_todos) * 100, 1)
    else:
        todo_completion_rate = 0
    
    # Priority breakdown
    priority_breakdown = {
        'high': Todo.objects.filter(user=user, priority='high').count(),
        'medium': Todo.objects.filter(user=user, priority='medium').count(),
        'low': Todo.objects.filter(user=user, priority='low').count(),
    }
    
    # ===== ACHIEVEMENTS =====
    
    achievements = Achievement.objects.filter(user=user).order_by('-earned_date')
    total_achievements = achievements.count()
    recent_achievements = achievements[:5]
    
    # Weekly summary (last 7 days)
    week_start = today - timedelta(days=6)
    weekly_completions = HabitCompletion.objects.filter(
        habit__user=user,
        date__gte=week_start,
        date__lte=today,
        completed=True
    ).count()
    
    weekly_habits_count = habits.count() * 7
    if weekly_habits_count > 0:
        weekly_completion_rate = round((weekly_completions / weekly_habits_count) * 100, 1)
    else:
        weekly_completion_rate = 0
    
    context = {
        'total_habits': total_habits,
        'total_completions': total_completions,
        'longest_streak': longest_streak,
        'longest_streak_habit': longest_streak_habit,
        'total_achievements': total_achievements,
        'weekly_completion_rate': weekly_completion_rate,
        
        # Chart data (converted to JSON for JavaScript)
        'dates_labels': json.dumps(dates_labels),
        'daily_completions': json.dumps(daily_completions),
        'category_labels': json.dumps(list(category_data.keys())),
        'category_values': json.dumps(list(category_data.values())),
        'category_percentages': category_percentages,
        
        'best_habits': best_habits,
        'recent_achievements': recent_achievements,
        
        # Todo stats
        'total_todos': total_todos,
        'completed_todos': completed_todos,
        'pending_todos': pending_todos,
        'todo_completion_rate': todo_completion_rate,
        'priority_breakdown': priority_breakdown,
    }
    
    return render(request, 'dashboard/analytics.html', context)