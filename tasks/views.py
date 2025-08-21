from django.shortcuts import render, redirect
from tasks.forms import TaskDetailModelForm, TaskForm, TaskModelForm
from tasks.models import Tasks, TaskDetail, Project
from django.db.models import Q, Count, Avg, Max, Min
from django.http import HttpResponse
from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.decorators import method_decorator
from users.views import is_admin
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import ContextMixin


class Greetings(View):
    greetings = "Hello, World!"

    def get(self, request):
        return HttpResponse(self.greetings)
    
class HiGreetings(Greetings):
    greetings = "Hi, World!"

class HelloGreetings(Greetings):
    greetings = "Hello, World, How are you ?"


def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()

# Create your views here.

user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):
    # Getting Task Count
    # total_task = tasks.count()
    # completed_task = Tasks.objects.filter(status="COMPLETED").count()
    # in_progress_task = Tasks.objects.filter(status="IN_PROGRESS").count()
    # pending_task = Tasks.objects.filter(status="PENDING").count()
    
    type = request.GET.get('type', 'all')

    counts = Tasks.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status="COMPLETED")),
        in_progress=Count('id', filter=Q(status="IN_PROGRESS")),
        pending=Count('id', filter=Q(status="PENDING")),
        )
    
    # Retriving task data
    base_query = Tasks.objects.select_related('task_detail').prefetch_related('assigned_to')

    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in-progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type == 'all':
        tasks = base_query.all()

    context = {
        "tasks": tasks,
        "counts": counts,
        "role": 'manager'    
        }
    return render(request, "dashboard/manager-dashboard.html", context)

@user_passes_test(is_employee, login_url='no-permission')
def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    context = {
        "names": ["Mahmud", "Ahmed", "John", "Shajib", "Rajib"],
        "Fahad": {"name": "Md. Fahad Monshi", "eye": "blue"}
    }
    return render(request, "test.html", context)

@login_required
@permission_required('tasks.add_tasks', login_url='no-permission')
def create_task(request):
    task_form = TaskModelForm() # For GET Request
    task_detail_form = TaskDetailModelForm()

    if request.method == "POST": # For POST Request
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():
            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Created Successfully!")
            return redirect('create-task')

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)

# Decorators for views
# @method_decorator(login_required, name='dispatch')
# @method_decorator(permission_required('tasks.add_tasks', login_url='no-permission'), name='dispatch')
# decorators = [login_required, permission_required('tasks.add_tasks', login_url='no-permission')]
# @method_decorator(decorators, name='dispatch')

class CreateTask(LoginRequiredMixin, PermissionRequiredMixin, ContextMixin, View):
    permission_required = 'tasks.add_tasks'
    login_url = 'sign-in'

    """ For creating task using Class Based View """
    task_model_form = TaskModelForm
    task_detail_model_form = TaskDetailModelForm
    template_name = "task_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = kwargs.get('task_form', self.task_model_form())
        context['task_detail_form'] = kwargs.get('task_detail_form', self.task_detail_model_form())
        return context

    def get(self, request, *args, **kwargs):
        task_form = self.task_model_form() # For GET Request
        task_detail_form = self.task_detail_model_form()
        # context = {"task_form": task_form, "task_detail_form": task_detail_form}
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task_form = self.task_model_form(request.POST)
        task_detail_form = self.task_detail_model_form(request.POST, request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, "Task Created Successfully!")
            context = self.get_context_data(task_form=task_form, task_detail_form=task_detail_form)
            return render(request, self.template_name, context)
            # return redirect('create-task')

@login_required
@permission_required('tasks.view_tasks', login_url='no-permission')
def view_task(request):
    """ 
    # Show completed tasks
    task = Tasks.objects.filter(status="COMPLETED")
    """
    """ 
    # Show Todays Tasks
    tasks = Tasks.objects.filter(due_date=date.today())
    """

    """ # Show tasks with low priority
    tasks = TaskDetail.objects.exclude(priority="H")
    return render(request, "show_task.html", {"tasks": tasks}) """

    """ # Show the task that contains word paper
    tasks = Tasks.objects.filter(title__icontains = "we", status__icontains="completed") """

    """ # Show the task which are pending or in progress
    tasks = Tasks.objects.filter(Q(status="PENDING") | Q(status="IN_PROGRESS")) """
    """ 
    # To check if any result exists
    tasks = Tasks.objects.filter(status="COMPLETED").exists() """
    """ 
    # Retrieve all data from tasks model
    tasks = Tasks.objects.all()
    # task3 = Tasks.objects.get(id=3)
    # task3 = Tasks.objects.get(pk=3)

    # Fetch the first task
    task3 = Tasks.objects.first()
    return render(request, "show_task.html", {"tasks": tasks, "task3": task3})
    """
    
    """ Select related (ForeignKey, OneToOneField) """
    # tasks = Tasks.objects.select_related('task_detail').all()
    # tasks = TaskDetail.objects.select_related('task').all()
    # tasks = Tasks.objects.select_related('project').all()
    
    """ prefetch_related (reverce foreignkey, many to many) """
    # tasks = Project.objects.prefetch_related("tasks").all()
    # tasks = Tasks.objects.prefetch_related("assigned_to").all()
    # tasks = Employee.objects.prefetch_related("tasks").all()

    """ Aggregate """
    # tasks = Tasks.objects.aggregate(num_task=Count('id'))
    tasks = Project.objects.annotate(num_task=Count('tasks')).order_by('num_task')
    return render(request, "show_task.html", {"tasks": tasks})

@login_required
@permission_required('tasks.change_tasks', login_url='no-permission')
def update_task(request, id):
    task = Tasks.objects.get(id=id)
    task_form = TaskModelForm(instance=task)

    # Handle missing task_detail
    try:
        task_detail = task.task_detail
    except TaskDetail.DoesNotExist:
        task_detail = None

    task_detail_form = TaskDetailModelForm(instance=task_detail) if task_detail else TaskDetailModelForm()

    if request.method == 'POST':
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(request.POST, instance=task.task_detail)

        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect('update-task', id=id)
        
    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, 'task_form.html', context)

# Delete Task view
@login_required
@permission_required('tasks.delete_tasks', login_url='no-permission')
def delete_task(request, id):
    if request.method == 'POST':
        task = Tasks.objects.get(id=id)
        task.delete()
        messages.success(request, "Task Deleted Successfully")
        return redirect('manager-dashboard')
    else:
        messages.error(request, "Something went wrong")
        return redirect('manager-dashboard')

@login_required
@permission_required('tasks.view_tasks', login_url='no-permission')
def task_details(request, task_id):
    task = Tasks.objects.get(id=task_id)
    status_choices = Tasks.STATUS_CHOICES

    if request.method == 'POST':
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        if selected_status in [status[0] for status in status_choices]:
            task.status = selected_status
            task.save()
            return redirect('task-details', task_id=task_id)
        # task.save()

    return render(request, 'task_details.html', {'task': task, 'status_choices': status_choices})

@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager-dashboard')
    elif is_employee(request.user):
        return redirect('user-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')

    return redirect('no-permission')