from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Habit, HabitCompletion
from .forms import HabitForm
from .achievement_service import check_and_award_achievements

@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user, is_active=True)
    return render(request, 'habits/habit_list.html', {'habits': habits})

@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, 'Habit created successfully!')
            return redirect('dashboard')
    else:
        form = HabitForm()
    
    return render(request, 'habits/habit_form.html', {'form': form, 'title': 'Create Habit'})

@login_required
def habit_update(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Habit updated successfully!')
            return redirect('dashboard')
    else:
        form = HabitForm(instance=habit)
    
    return render(request, 'habits/habit_form.html', {'form': form, 'title': 'Update Habit'})

@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    
    if request.method == 'POST':
        habit.is_active = False
        habit.save()
        messages.success(request, 'Habit deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'habits/habit_confirm_delete.html', {'habit': habit})

@login_required
def habit_complete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    today = timezone.now().date()
    
    # Get or create today's completion
    completion, created = HabitCompletion.objects.get_or_create(
        habit=habit,
        date=today,
        defaults={'completed': True}
    )
    
    if not created:
        # Toggle completion
        completion.completed = not completion.completed
        completion.save()
    
    # Check for new achievements
    new_achievements = check_and_award_achievements(request.user)
    
    if completion.completed:
        messages.success(request, f'Great job! {habit.name} completed for today! 🎉')
        
        # Notify about new achievements
        for achievement in new_achievements:
            messages.success(
                request, 
                f'🏆 Achievement Unlocked: {achievement.get_achievement_type_display()}!'
            )
    else:
        messages.info(request, f'{habit.name} marked as incomplete.')
    
    return redirect('dashboard')