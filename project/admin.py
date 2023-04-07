from django.contrib import admin

from project.models import Project, Task, Category


admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Task)
