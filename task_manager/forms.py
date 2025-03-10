from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Comment, MessageNew, Position, Project, Task, Team


class ReplyMassageForm(forms.ModelForm):
    class Meta:
        model = MessageNew
        fields = ("title", "content")
        labels = {
            "title": "Title",
            "content": "Content",
        }
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.to_worker = kwargs.pop("to_worker", None)
        super().__init__(*args, **kwargs)

        
    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        if self.request:
            instance.from_worker = self.request.user
        if self.to_worker:    
            instance.to_worker = self.to_worker
        instance.save()
        return instance
    
    
class AddComentaryForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        labels = {
            "content": "Comment",
        }
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.task = kwargs.pop("task", None)
        super().__init__(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        if self.request:
            instance.worker = self.request.user
        if self.task:
            instance.task = self.task
        instance.save()
        return instance
    
    
class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name", "description", "start_date", "end_date", "is_complited", "priority")
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"})
        }
    
    
class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name", "task_type", "description", "deadline", "priority", "is_complited", "assignees")
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date", "class": "form-control"})
        }
        
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={
            "class": "form-control"
        })
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )
    
    position_name = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )
    team_name = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }
            
    def save(self):
        worker = super().save(commit=False)
        worker.set_password(self.cleaned_data["password1"])
        worker.is_active = True

        position, _ = Position.objects.get_or_create(name=self.cleaned_data["position_name"])
        worker.position = position

        team, _ = Team.objects.get_or_create(name=self.cleaned_data["team_name"])
        worker.team = team
        
        worker.save()
        return worker
