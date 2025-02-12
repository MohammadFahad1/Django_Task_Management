from django.shortcuts import render
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Tasks, TaskDetail, Project
from django.db.models import Q
from django.http import HttpResponse
from datetime import date
# Create your views here.

def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    context = {
        "names": ["Mahmud", "Ahmed", "John", "Shajib", "Rajib"],
        "Fahad": {"name": "Md. Fahad Monshi", "eye": "blue"}
    }
    return render(request, "test.html", context)

def create_task(request):
    # employees = Employee.objects.all()
    form = TaskModelForm() # For GET Request

    if request.method == "POST": # For POST Request
        form = TaskModelForm(request.POST)
        if form.is_valid():
            """ For Model Form Data """
            form.save()
            return render(request, "task_form.html", {"form": form, "message": "Task Added Successfully!"})

            """ For Django Form Data """
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to')

            # task = Tasks.objects.create(title=title, description=description, due_date=due_date)
            # # Assign employees to task
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            
            # return HttpResponse("Task added successfully")

    context = {"form": form}
    return render(request, "task_form.html", context)

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
    tasks = Employee.objects.prefetch_related("tasks").all()
    return render(request, "show_task.html", {"tasks": tasks})