from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import TaskForm, SimpleSearchForm
from webapp.models import Task


class TasksView(ListView):
    template_name = 'task/tasks.html'

    context_object_name = 'tasks'
    model = Task
    ordering = ['-updated_at']

    paginate_by = 9
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_deleted=True)
        if self.search_value:
            query = Q(title__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class TaskDetailView(DetailView):
    template_name = 'task/task_detail.html'
    model = Task

    def get(self, request, *args, **kwargs):
        context = super().get(request, *args, **kwargs)
        task = get_object_or_404(Task, pk=kwargs['pk'])
        if task.is_deleted == True:
            raise Http404
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = self.object.type.all()
        return context


class TaskAddView(LoginRequiredMixin, CreateView):
    template_name = 'task/add_task.html'
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse('detail_view', kwargs={'pk': self.object.pk})


class TaskUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'task/update_task.html'
    form_class = TaskForm
    model = Task
    permission_denied_message = 'У вас нет прав доступа'

    def test_func(self):
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        return self.request.user.has_perm('webapp.change_task') and \
            task.project.user.filter(pk=self.request.user.pk).exists()

    def get_success_url(self):
        return reverse('detail_view', kwargs={'pk': self.object.pk})


class TaskDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'task/confirm_delete.html'
    model = Task
    success_url = reverse_lazy('tasks_view')
    permission_denied_message = 'У вас нет прав доступа'

    def test_func(self):
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        return self.request.user.has_perm('webapp.delete_task') and \
            task.project.user.filter(pk=self.request.user.pk).exists()
