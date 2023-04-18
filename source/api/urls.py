from django.urls import path

from api.views import TaskListView, TaskDetailUpdateDeleteView, ProjectDetailUpdateDeleteView

urlpatterns = [
    # URL для задач
    path('tasks/', TaskListView.as_view(), name='api_tasks_list'),
    path('tasks/<int:pk>/', TaskDetailUpdateDeleteView.as_view(), name='api_task_detail'),

    # URL для проектов
    path('project/<int:pk>/', ProjectDetailUpdateDeleteView.as_view(), name='api_project_list')
]
