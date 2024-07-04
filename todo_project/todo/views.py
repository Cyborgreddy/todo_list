from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Task
from .forms import TaskForm
from datetime import datetime

def task_list(request):
    tasks = Task.objects.all()

    # Update status of expired tasks
    for task in tasks:
        task.check_and_update_status()

    query = request.GET.get('q')
    if query:
        tasks = tasks.filter(task__icontains=query)

    date_query = request.GET.get('date')
    if date_query:
        try:
            date_obj = datetime.strptime(date_query, '%Y-%m-%d').date()
            tasks = tasks.filter(due_date=date_obj)
        except ValueError:
            tasks = Task.objects.none()

    form = TaskForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('task_list')

    return render(request, 'task_list.html', {'tasks': tasks, 'form': form})

def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('task_list')
    return render(request, 'edit_task.html', {'form': form})

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'delete_task.html', {'task': task})

def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = 'completed'
    task.save()
    return redirect('task_list')
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')  
    else:
        form = TaskForm()
    
    return render(request, 'task_list.html', {'form': form})