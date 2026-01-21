from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from habits.models import Habit
from todos.models import Todo
from django.db.models import Count, Q

@login_required
def dashboard(request):
    # Get user's habits
    habits = Habit.objects.filter(user=request.user, is_active=True)
    
    # Get user's todos
    todos_pending = Todo.objects.filter(user=request.user, completed=False)
    todos_completed = Todo.objects.filter(user=request.user, completed=True)
    
    # Calculate statistics
    total_habits = habits.count()
    habits_completed_today = sum(1 for habit in habits if habit.is_completed_today())
    
    total_todos = Todo.objects.filter(user=request.user).count()
    todos_pending_count = todos_pending.count()
    todos_completed_count = todos_completed.count()
    
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
        'habits': habits,
        'todos_pending': todos_pending[:5],  # Show only 5 pending todos
        'todos_completed': todos_completed[:5],  # Show only 5 completed todos
        'total_habits': total_habits,
        'habits_completed_today': habits_completed_today,
        'total_todos': total_todos,
        'todos_pending_count': todos_pending_count,
        'todos_completed_count': todos_completed_count,
        'habit_completion_percentage': round(habit_completion_percentage, 1),
        'todo_completion_percentage': round(todo_completion_percentage, 1),
    }
    
    return render(request, 'dashboard/dashboard.html', context)