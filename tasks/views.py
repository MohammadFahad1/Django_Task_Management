from django.shortcuts import render
from tasks.forms import TaskForm
from tasks.models import Employee, Tasks
from django.http import HttpResponse
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
    employees = Employee.objects.all()
    form = TaskForm(employees = employees) # For GET Request
    if request.method == "POST":
        form = TaskForm(request.POST, employees = employees)
        if form.is_valid():
            data = form.cleaned_data
            title = data.get('title')
            description = data.get('description')
            due_date = data.get('due_date')
            assigned_to = data.get('assigned_to')

            task = Tasks.objects.create(title=title, description=description, due_date=due_date)
            # Assign employees to task
            for emp_id in assigned_to:
                employee = Employee.objects.get(id=emp_id)
                task.assigned_to.add(employee)
            
            return HttpResponse("Task added successfully")

    context = {"form": form}
    return render(request, "task_form.html", context)