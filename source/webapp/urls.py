from django.urls import path
from webapp.views.base import IndexView
from webapp.views.projects import (
    ProjectsView, ProjectDetailView, ProjectCreateView,
    ProjectTaskCreateView, ProjectUpdateView, ProjectAddUserView, ProjectDeleteUserView
)
from webapp.views.tasks import (
    TaskAddView, TaskDetailView, TaskUpdateView,
    TaskDeleteView, TasksView
)

urlpatterns = [
    # URL для задач
    path('', IndexView.as_view(), name='index'),
    path('tasks', TasksView.as_view(), name='tasks_view'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='detail_view'),
    path('tasks/add', TaskAddView.as_view(), name='add_view'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('task/<int:pk>/confirm_delete/', TaskDeleteView.as_view(), name='confirm_delete'),

    # URL для проектов
    path('projects', ProjectsView.as_view(), name='projects_view'),
    path('projects/<int:pk>/tasks/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/add', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/update', ProjectUpdateView.as_view(), name='project_update'),
    path('project/<int:pk>/tasks/add', ProjectTaskCreateView.as_view(), name='project_add_task'),
    path('project/<int:pk>/users/add', ProjectAddUserView.as_view(), name='project_add_user'),
    path('project/<int:pk>/users/delete', ProjectDeleteUserView.as_view(), name='project_delete_user')
]
