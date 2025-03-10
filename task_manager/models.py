from django.db import models
from django.contrib.auth.models import AbstractUser


class TaskType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Team(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    
class Position(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    
class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True) 
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True) 
    
    def __str__(self):
        return f"{self.username} - {self.team}"
    
    
class PriorityChoices(models.TextChoices):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
    
class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_complited = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PriorityChoices.choices, 
        default=PriorityChoices.LOW
        )
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} - {self.team}"
    

class Task(models.Model): 
    name = models.CharField(max_length=50)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_complited = models.BooleanField(default=False)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    priority = models.CharField(
        max_length=10, 
        choices=PriorityChoices, 
        default=PriorityChoices.LOW
        )
    assignees = models.ManyToManyField(Worker)
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name="tasks"
        )
    
    def __str__(self):
        return f"{self.name} - {self.project}"
    

class MessageNew(models.Model):
    from_worker = models.ForeignKey(
        Worker, 
        on_delete=models.CASCADE, 
        related_name="from_worker"
        )  
    to_worker = models.ForeignKey(
        Worker, 
        on_delete=models.CASCADE, 
        related_name="to_worker"
        )
    title = models.CharField(max_length=255)
    content = models.TextField()
    send_datetime = models.DateTimeField(auto_now_add=True)    
    is_read = models.BooleanField(default=False)
    is_archieve = models.BooleanField(default=False)
    
    
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    content = models.TextField()
    send_datetime = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.worker} - {self.task}"
