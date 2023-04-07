from django.urls import path

from .views import ProjectListView, TaskListView, ProjectDetailsView, TaskDetailsView, CategoryListView, \
    CategoryDetailView

urlpatterns = [
    path('category/', CategoryListView.as_view()),  # Список всех категорий
    path('category/<int:pk>/', CategoryDetailView.as_view()),  # Изменение, удаление категории
    path('projectlist/<int:pk>/', ProjectListView.as_view()),   # Список всех проектов относящихся к категории
    path('project/<int:pk>/', ProjectDetailsView.as_view()),   # Возвращает конкретный проект
    path('project/tasklist/<int:pk>/', TaskListView.as_view()),   # Список всех задач проекта
    path('project/task/<int:pk>/', TaskDetailsView.as_view()),   # Возвращает конкретную задачу
]