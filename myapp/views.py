from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Task
from django.contrib.auth.decorators import login_required
from .forms import TaskForm

def index(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
    else:
        tasks = Task.objects.none()  # or redirect to login page, etc.

    return render(request, 'myapp/index.html', {'tasks': tasks})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('myapp:index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'myapp/login.html')

def logout_view(request):
    logout(request)
    return redirect('myapp:index')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('myapp:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'myapp/register.html', {'form': form})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('myapp:index')  # Redirect to the task list or another page
    else:
        form = TaskForm()
    return render(request, 'myapp/add_task.html', {'form': form})

def edit_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('myapp:index')
    else:
        form = TaskForm(instance=task)
    return render(request, 'myapp/edit_task.html', {'form': form, 'task': task})

def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()
    return redirect('myapp:index')


def task_detail(request, id):
    task = get_object_or_404(Task, id=id)
    return render(request, 'myapp/task_detail.html', {'task': task})