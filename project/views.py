from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .permissions import IsAdminOrReadOnly
from .serializers import ProjectsListSerializer, TaskListSerializer, CategoryListSerializer
from .models import Project, Task, Category


class CategoryListView(generics.ListCreateAPIView):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser, )
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class ProjectListView(generics.ListCreateAPIView):
    permission_classes = (IsAdminOrReadOnly, )
    serializer_class = ProjectsListSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Project.objects.filter(category__pk=pk)


class ProjectDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser, )
    queryset = Project.objects.all()
    serializer_class = ProjectsListSerializer


class TaskListView(generics.ListCreateAPIView):
    permission_classes = (IsAdminOrReadOnly, )
    serializer_class = TaskListSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Task.objects.filter(project__pk=pk)


class TaskDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer



