from asyncio import Task
from django.db import models
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

# Create your models here.
class Tasks(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed')
    ]
    
    """
    Create your own primary key
    ---------------------------
    std_id = models.CharField(max_length=200, primary_key=True)
    """
    project = models.ForeignKey("Project", on_delete=models.CASCADE, default=1, related_name="tasks")
    assigned_to = models.ManyToManyField(Employee, related_name="tasks")
    title = models.CharField(max_length=250, default="")
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="PENDING")
    is_completed = models.BooleanField(default=False)
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
    task = models.OneToOneField(Tasks, on_delete=models.CASCADE, related_name="task_detail")
    # assigned_to = models.CharField(max_length=100)
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

# task = onekgula employee ekta task
# employee = onekgula task er jonno assign ache

# Signals
""" @receiver(post_save, sender=Tasks)
def notify_task_creation(sender, instance, created, **kwargs):
    print("sender", sender)
    print("instance", instance)
    print(kwargs)
    print("created", created)
    if created:
        instance.is_completed = True
        instance.save() """

""" @receiver(pre_save, sender=Tasks)
def notify_task_creation(sender, instance, **kwargs):
    print("sender", sender)
    print("instance", instance)
    print(kwargs)
    
    instance.is_completed = True """

@receiver(m2m_changed, sender=Tasks)
def notify_employees_on_task_creation(sender, instance, created, **kwargs):
    if created:
        assigned_emails = [emp.email for emp in instance.assigned_to.all()]
        print("Checking", instance)
        send_mail(
            "New Task Assigned",
            "You have been assigned to the task: {instance.title}",
            "36fahad@gmail.com",
            assigned_emails,
            fail_silently=False,
        )