from django.db import models
from django.conf import settings
from django.utils import timezone

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks')

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.ManyToManyField(Task, related_name='categories')
    
    def __str__(self):
        return self.name


class Interaction(models.Model):
    ACTION_CHOICES = [
        ('ADD', 'Add'),
        ('MODIFY', 'Modify'),
        ('DELETE', 'Delete'),
        ('MOVE', 'Move to other task'),
    ]
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.get_action_display()} by {self.user.username} on {self.task.title}"


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.title}"