from django.urls import path

from api.views import TaskListView, TaskDetailUpdateDeleteView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='api_tasks_list'),
    path('tasks/<int:pk>/', TaskDetailUpdateDeleteView.as_view(), name='api_task_detail')
]