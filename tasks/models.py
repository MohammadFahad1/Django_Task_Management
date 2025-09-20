from asyncio import Task
from django.db import models
from django.conf import settings
# Create your models here.
class Tasks(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]
    
    """
    Create your own primary key
    ---------------------------
    std_id = models.CharField(max_length=200, primary_key=True)
    """
    project = models.ForeignKey("Project", on_delete=models.CASCADE, default=1, related_name="tasks")
    # assigned_to = models.ManyToManyField(Employee, related_name="tasks")
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasks")
    title = models.CharField(max_length=250, default="")
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TaskDetail(models.Model):
    HIGH = "H"
    MEDIUM = "M"
    LOW = "L"
    PRIORITY_OPTIONS = (
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low")
    )
    # task = models.OneToOneField(Tasks, on_delete=models.CASCADE, related_name="task_detail")
    task = models.OneToOneField(Tasks, on_delete=models.DO_NOTHING, related_name="task_detail")
    # assigned_to = models.CharField(max_length=100)
    asset = models.ImageField(upload_to="tasks_assets", blank=True, null=True, default='tasks_assets/default_image.png')
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Details of task: {self.task.title}"

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name

