from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from habits.models import Habit, Achievement
from habits.achievement_service import get_user_points
from todos.models import Todo
from django.db.models import Count, Q

@login_required
def dashboard(request):
    # Get user's habits
    all_habits = Habit.objects.filter(user=request.user, is_active=True)
    
    # Get ONLY uncompleted habits for today
    uncompleted_habits = [habit for habit in all_habits if not habit.is_completed_today()]
    
    # Get user's todos - ONLY uncompleted
    todos_pending = Todo.objects.filter(user=request.user, completed=False)[:10]
    
    # Get recently completed todos for the sidebar (last 5)
    todos_completed = Todo.objects.filter(user=request.user, completed=True).order_by('-completed_at')[:5]
    
    # Get user's achievements
    achievements = Achievement.objects.filter(user=request.user).order_by('-earned_date')[:6]
    total_achievements = Achievement.objects.filter(user=request.user).count()
    
    # Calculate user points
    user_points = get_user_points(request.user)
    
    # Calculate statistics
    total_habits = all_habits.count()
    habits_completed_today = sum(1 for habit in all_habits if habit.is_completed_today())
    
    total_todos = Todo.objects.filter(user=request.user).count()
    todos_pending_count = Todo.objects.filter(user=request.user, completed=False).count()
    todos_completed_count = Todo.objects.filter(user=request.user, completed=True).count()
    
    # Calculate completion percentage
    if total_habits > 0:
        habit_completion_percentage = (habits_completed_today / total_habits) * 100
    else:
        habit_completion_percentage = 0
    
    if total_todos > 0:
        todo_completion_percentage = (todos_completed_count / total_todos) * 100
    else:
        todo_completion_percentage = 0
    
    context = {
        'habits': uncompleted_habits,  # Only uncompleted habits
        'all_habits': all_habits,  # For stats
        'todos_pending': todos_pending,
        'todos_completed': todos_completed,
        'achievements': achievements,
        'total_achievements': total_achievements,
        'user_points': user_points,
        'total_habits': total_habits,
        'habits_completed_today': habits_completed_today,
        'uncompleted_habits_count': len(uncompleted_habits),
        'total_todos': total_todos,
        'todos_pending_count': todos_pending_count,
        'todos_completed_count': todos_completed_count,
        'habit_completion_percentage': round(habit_completion_percentage, 1),
        'todo_completion_percentage': round(todo_completion_percentage, 1),
    }
    
    return render(request, 'dashboard/dashboard.html', context)