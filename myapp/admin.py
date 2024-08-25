from django.contrib import admin
from .models import Task, Category, Interaction, Comment
from .forms import TaskForm
    
class TaskAdmin(admin.ModelAdmin):
    form = TaskForm
    list_display = ('title', 'description', 'completed', 'user', 'created_at', 'due_at', 'priority', 'parent_task')
    list_filter = ('completed', 'priority', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)  # Fields that should be read-only

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)
    filter_horizontal = ('task',)  # For many-to-many relationships

class InteractionAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'action', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('task__title', 'user__username', 'action')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__username', 'task__title')

# Register models with the admin site
admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Interaction, InteractionAdmin)
admin.site.register(Comment, CommentAdmin)