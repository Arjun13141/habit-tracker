from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Todo
from .forms import TodoForm

@login_required
# def todo_list(request):
#     todos = Todo.objects.filter(user=request.user)
#     return render(request, 'todos/todo_list.html', {'todos': todos})
def todo_list(request):
    todos = Todo.objects.filter(user=request.user)

    total_todos = todos.count()
    completed_todos = todos.filter(completed=True).count()
    pending_todos = total_todos - completed_todos

    return render(
        request,
        'todos/todo_list.html',
        {
            'todos': todos,
            'total_todos': total_todos,
            'completed_todos': completed_todos,
            'pending_todos': pending_todos,
        }
    )

@login_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Todo created successfully!')
            return redirect('dashboard')
    else:
        form = TodoForm()
    
    return render(request, 'todos/todo_form.html', {'form': form, 'title': 'Create Todo'})

@login_required
def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo updated successfully!')
            return redirect('dashboard')
    else:
        form = TodoForm(instance=todo)
    
    return render(request, 'todos/todo_form.html', {'form': form, 'title': 'Update Todo'})

@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Todo deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'todos/todo_confirm_delete.html', {'todo': todo})

@login_required
def todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    
    if todo.completed:
        todo.mark_incomplete()
        messages.info(request, f'{todo.title} marked as incomplete.')
    else:
        todo.mark_complete()
        messages.success(request, f'Great job! {todo.title} completed! ✅')
    
    return redirect('dashboard')