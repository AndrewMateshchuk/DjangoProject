from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import logout, login, authenticate
from .forms import RegistrationForm, LoginForm, TaskAddForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
import datetime

# Create your views here.


def index(request):
    context = {}
    if request.user.is_authenticated:
        date = datetime.date.today()
        tasks_high = Task.objects.filter(
            user__exact=request.user,
            date__exact=date,
            status__exact=False,
            priority__exact=Task.PRIORITY_HIGH)
        tasks_medium = Task.objects.filter(
            user__exact=request.user,
            date__exact=date,
            status__exact=False,
            priority__exact=Task.PRIORITY_MEDIUM)
        tasks_low = Task.objects.filter(
            user__exact=request.user,
            date__exact=date,
            status__exact=False,
            priority__exact=Task.PRIORITY_LOW)
        tasks_completed = Task.objects.filter(
            user__exact=request.user,
            date__exact=date,
            status__exact=True,)
        context = {
            'tasks_high': tasks_high,
            'tasks_medium': tasks_medium,
            'tasks_low': tasks_low,
            'tasks_completed': tasks_completed
        }
    return render(
        request,
        'TaskManager/index.html',
        context=context,
    )


def user_registration(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    form.add_error('username', form.error_massage)
        else:
            form = RegistrationForm()
        return render(request, 'registration/registration.html',
                      {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    form.add_error('username', form.error_massage)
        else:
            form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('index'))


def task_add(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TaskAddForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                description = form.cleaned_data.get('description')
                date = form.cleaned_data.get('date')
                priority = form.cleaned_data.get('priority')
                task = Task(
                    title=title,
                    description=description,
                    user=request.user,
                    date=date,
                    priority=priority)
                task.save()
                return HttpResponseRedirect(reverse('tasks'))
        else:
            form = TaskAddForm()
        return render(request, 'TaskManager/task_add.html', {'form': form})
    return HttpResponseRedirect(reverse('user-login'))


def task_delete(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        if task.user == request.user:
            task.delete()
            return HttpResponseRedirect(reverse('tasks'))
    return HttpResponseRedirect(reverse('index'))

def task_complete(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        if task.user == request.user:
            task.status = True
            task.save()
    return HttpResponseRedirect(reverse('index'))    


def task_edit(request, pk):
    if request.user.is_authenticated:
        task = get_object_or_404(Task, pk=pk)
        if task.user == request.user:
            if request.method == 'POST':
                form = TaskAddForm(request.POST)
                if form.is_valid():
                    task.title = form.cleaned_data.get('title')
                    task.description = form.cleaned_data.get('description')
                    task.date = form.cleaned_data.get('date')
                    task.priority = form.cleaned_data.get('priority')
                    task.save()
                    return HttpResponseRedirect(reverse('tasks'))
            else:
                form = TaskAddForm(instance=task)
                return render(request, 'TaskManager/task_edit.html',
                            {'form': form})
    return HttpResponseRedirect(reverse('user-login'))


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    login_url = 'user-login'
    redirect_field_name = 'redirect_to'
    paginate_by = 2

    def get_queryset(self):
        date = datetime.date.today()
        return Task.objects.filter(
            user__exact=self.request.user, date__gte=date,
            status__exact=False).order_by('date')


class ArchiveListView(LoginRequiredMixin, generic.ListView):
    model = Task
    login_url = 'user-login'
    redirect_field_name = 'redirect_to'
    paginate_by = 2

    def get_queryset(self):
        date = datetime.date.today()
        return Task.objects.filter(
            user__exact=self.request.user, date__lte=date).order_by('date')


class TaskDetailView(generic.DetailView):
    model = Task
    login_url = 'user-login'
    redirect_field_name = 'redirect_to'
