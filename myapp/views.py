from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Task
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from django.utils import timezone

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

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Task
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils import timezone

@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_at = request.POST.get('due_at')
        priority = request.POST.get('priority')
        parent_task_id = request.POST.get('parent_task')

        try:
            # Attempt to parse the date
            if due_at:
                due_at = timezone.datetime.strptime(due_at, "%Y-%m-%dT%H:%M")
            
            task = Task(
                user=request.user,
                title=title,
                description=description,
                due_at=due_at,
                priority=priority
            )

            if parent_task_id:
                parent_task = Task.objects.get(id=parent_task_id)
                task.parent_task = parent_task

            task.full_clean()  # This will run all validations
            task.save()
            messages.success(request, 'Task added successfully!')
            return redirect('myapp:index')
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
            else:
                for error in e.messages:
                    messages.error(request, error)
        except ValueError:
            messages.error(request, "Invalid date format. Please use the correct format.")

    # If it's a GET request or if there were errors in POST
    parent_tasks = Task.objects.filter(user=request.user, parent_task__isnull=True)
    return render(request, 'myapp/add_task.html', {'parent_tasks': parent_tasks})

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