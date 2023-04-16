from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, FormView
from webapp.forms import ProjectForm, ProjectTaskForm, ProjectAddUserForm, ProjectDeleteUserForm
from webapp.models import Project, Task


class ProjectsView(ListView):
    template_name = 'project/projects.html'

    context_object_name = 'projects'
    model = Project
    ordering = ['started_at']


class ProjectDetailView(ListView):
    template_name = 'project/project_detail.html'

    context_object_name = 'tasks'
    model = Task

    def get_queryset(self):
        self.project = Project.objects.get(pk=self.kwargs['pk'])
        queryset = super().get_queryset().exclude(is_deleted=True)
        return queryset.filter(project=self.project)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context


class ProjectCreateView(UserPassesTestMixin, CreateView):
    template_name = 'project/project_create.html'
    model = Project
    form_class = ProjectForm
    permission_denied_message = 'У вас нет прав доступа'

    def test_func(self):
        return self.request.user.has_perm('webapp.add_project')

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class ProjectTaskCreateView(UserPassesTestMixin, CreateView):
    model = Task
    template_name = 'project/project_task_create.html'
    form_class = ProjectTaskForm
    permission_denied_message = 'У вас нет прав доступа'

    def test_func(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return self.request.user.has_perm('webapp.add_task') and \
            Project.objects.filter(pk=project.pk, user=self.request.user).exists()

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        task = form.save(commit=False)
        task.project = project
        task.save()
        return redirect('project_detail', pk=project.pk)


class ProjectUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'project/project_update.html'
    form_class = ProjectForm
    model = Project
    permission_denied_message = 'У вас нет прав доступа'

    def test_func(self):
        return self.request.user.has_perm('webapp.change_project')

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class ProjectAddUserView(UserPassesTestMixin, FormView):
    template_name = 'project/project_add_user.html'
    form_class = ProjectAddUserForm
    model = Project
    permission_denied_message = 'У вас нет прав доступа'

    def test_func(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return self.request.user.has_perm('webapp.add_user_project') and \
            Project.objects.filter(pk=project.pk, user=self.request.user).exists()

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        user = get_object_or_404(User, pk=form.cleaned_data.get('user').pk)
        project.user.add(user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        context['project'] = project
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        project_id = self.kwargs.get('pk')
        return form_class(project_id, **self.get_form_kwargs())


class ProjectDeleteUserView(UserPassesTestMixin, FormView):
    template_name = 'project/project_delete_user.html'
    form_class = ProjectDeleteUserForm
    model = Project
    permission_denied_message = 'У вас нет прав доступа'

    def test_func(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return self.request.user.has_perm('webapp.delete_user_project') and \
            Project.objects.filter(pk=project.pk, user=self.request.user).exists()

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        user = get_object_or_404(User, pk=form.cleaned_data.get('user').pk)
        project.user.remove(user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        context['project'] = project
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        project_id = self.kwargs.get('pk')
        return form_class(project_id, **self.get_form_kwargs())
