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

@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_at = request.POST.get('due_at')
        priority = request.POST.get('priority')
        parent_task_id = request.POST.get('parent_task')

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

        task.save()
        return redirect('myapp:index')  # Redirect to the task list or another page
    else:
        parent_tasks = Task.objects.filter(user=request.user, parent_task__isnull=True)
        return render(request, 'myapp/add_task.html', {'parent_tasks': parent_tasks})

@login_required
def edit_task(request, id):
    # Fetch the task that needs to be edited
    task = get_object_or_404(Task, id=id, user=request.user)
    
    if request.method == 'POST':
        # Extract data from POST request
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_at = request.POST.get('due_at')
        priority = request.POST.get('priority')
        completed = request.POST.get('completed') == 'on'  # Checkbox handling
        parent_task_id = request.POST.get('parent_task')

        # Update the task object
        task.title = title
        task.description = description
        task.due_at = due_at
        task.priority = priority
        task.completed = completed

        # Handle parent task
        if parent_task_id:
            parent_task = Task.objects.get(id=parent_task_id)
            task.parent_task = parent_task
        else:
            task.parent_task = None

        # Save the changes to the task
        task.save()

        # Redirect after successful update
        return redirect('myapp:index')  # Redirect to the task list or another page
    else:
        # Fetch parent tasks excluding the task being edited
        parent_tasks = Task.objects.filter(user=request.user, parent_task__isnull=True).exclude(id=id)
        
        # Render the edit task form
        return render(request, 'myapp/edit_task.html', {
            'task': task,
            'parent_tasks': parent_tasks
        })
   
def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()
    return redirect('myapp:index')


def task_detail(request, id):
    task = get_object_or_404(Task, id=id)
    return render(request, 'myapp/task_detail.html', {'task': task})