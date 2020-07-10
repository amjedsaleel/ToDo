from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import *
# Create your views here.


def index(request):
    tasks = Task.objects.all()
    total_tasks = Task.objects.all().count()
    remaining_tasks = Task.objects.exclude(complete=True).count()
    form = TaskForm()
    if request.method == 'POST' and 'add-task' in request.POST:
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')

    if request.method == 'POST' and 'delete-all-task' in request.POST:
        Task.objects.all().delete()
        return redirect('/')

    context = {
        'tasks': tasks,
        'form': form,
        'total_tasks': total_tasks,
        'remaining_tasks': remaining_tasks,
    }
    return render(request, 'tasks/list.html', context)


def update_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect('/')
    context = {'form': form}
    return render(request, 'tasks/update_task.html', context)


def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    context = {'task': task}
    return render(request, 'tasks/delete.html', context)
