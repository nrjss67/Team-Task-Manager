from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse, reverse_lazy
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin

from task_manager.context_processors import get_slugify_team_name
from task_manager.forms import (
    AddComentaryForm,
    ProjectCreateForm,
    ReplyMassageForm,
    SignUpForm,
    TaskCreateForm,
)
from .models import Project, Task, MessageNew


class IndexView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            team_name = get_slugify_team_name(request)["team_name"]
            return redirect(
                reverse_lazy("task_manager:home_page", kwargs={"team_name": team_name})
            )
        return redirect("login")


class LoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        team_name = get_slugify_team_name(self.request)["team_name"]
        return reverse_lazy("task_manager:home_page", kwargs={"team_name": team_name})


class SignUpView(generic.CreateView):
    model = get_user_model()
    form_class = SignUpForm
    template_name = "registration/sign-up.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = authenticate(
            self.request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        if user is not None:
            login(self.request, user)
        return response

    def get_success_url(self):
        team_name = get_slugify_team_name(self.request)
        return reverse_lazy("task_manager:home_page", kwargs={"team_name": team_name})


class LogoutView(LogoutView):
    next_page = reverse_lazy("login")


class PersonalTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "task_manager/personal_task_list.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        context = Task.objects.filter(
            assignees__username__icontains=self.request.user.username
        )
        status = self.request.GET.get("status")
        priority = self.request.GET.get("priority")
        search = self.request.GET.get("search")

        if status == "completed":
            context = context.filter(is_complited=True)
        if status == "not_completed":
            context = context.filter(is_complited=False)
        if priority == "low":
            context = context.filter(priority="low")
        if priority == "medium":
            context = context.filter(priority="medium")
        if priority == "high":
            context = context.filter(priority="high")
        if search:
            context = context.filter(name__icontains=search)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = self.request.GET.get("status", "all")
        context["priority"] = self.request.GET.get("priority", "all")
        return context


class TeamProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    template_name = "task_manager/team_project_list.html"
    context_object_name = "projects"
    paginate_by = 10

    def get_queryset(self):
        context = Project.objects.filter(team=self.request.user.team)
        status = self.request.GET.get("status")
        priority = self.request.GET.get("priority")
        search = self.request.GET.get("search")

        if status == "completed":
            context = context.filter(is_complited=True)
        if status == "pending":
            context = context.filter(is_complited=False)
        if priority == "low":
            context = context.filter(priority="low")
        if priority == "medium":
            context = context.filter(priority="medium")
        if priority == "high":
            context = context.filter(priority="high")
        if search:
            context = context.filter(name__icontains=search)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = self.request.GET.get("status", "all")
        context["priority"] = self.request.GET.get("priority", "all")
        context["completed_projects"] = Project.objects.filter(
            is_complited=True
        ).count()
        context["active_projects"] = Project.objects.filter(is_complited=False).count()
        context["team_workers"] = self.request.user.team.worker_set.count()
        return context


class TeamProjectTaskListView(LoginRequiredMixin, generic.ListView):
    model = Project
    template_name = "task_manager/team_project_task_list.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_context_data(self):
        context = super().get_context_data()
        context["project"] = Project.objects.get(pk=self.kwargs["pk_project"])
        context["completed_tasks"] = (
            Project.objects.get(pk=self.kwargs["pk_project"])
            .tasks.filter(is_complited=True)
            .count()
        )
        context["not_completed_tasks"] = (
            Project.objects.get(pk=self.kwargs["pk_project"])
            .tasks.filter(is_complited=False)
            .count()
        )
        context["high_priority_tasks"] = (
            Project.objects.get(pk=self.kwargs["pk_project"])
            .tasks.filter(priority="high")
            .count()
        )
        return context

    def get_queryset(self):
        queryset = Project.objects.get(pk=self.kwargs["pk_project"]).tasks.all()
        search = self.request.GET.get("search")
        priority = self.request.GET.get("priority")
        status = self.request.GET.get("status")

        if priority == "low":
            queryset = queryset.filter(priority="low")
        if priority == "medium":
            queryset = queryset.filter(priority="medium")
        if priority == "high":
            queryset = queryset.filter(priority="high")
        if status == "completed":
            queryset = queryset.filter(is_complited=True)
        if status == "pending":
            queryset = queryset.filter(is_complited=False)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView, generic.edit.FormMixin):
    model = Task
    template_name = "task_manager/team_project_task_detail.html"
    context_object_name = "task"
    pk_url_kwarg = "pk_task"
    form_class = AddComentaryForm

    def get_queryset(self):
        context = Task.objects.filter(pk=self.kwargs["pk_task"])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request, "task": self.get_queryset()[0]})
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

    def get_success_url(self):
        return reverse_lazy(
            "task_manager:team_project_task_detail",
            kwargs={
                "team_name": get_slugify_team_name(self.request)["team_name"],
                "pk_project": self.kwargs["pk_project"],
                "pk_task": self.kwargs["pk_task"],
            },
        )


class CreateProjectView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = "task_manager/create_project.html"

    def get_success_url(self):
        team_name = get_slugify_team_name(self.request)["team_name"]
        return reverse(
            "task_manager:team_projects_list", kwargs={"team_name": team_name}
        )

    def form_valid(self, form):
        form.instance.team = self.request.user.team
        return super().form_valid(form)


class UpdateProjectView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = "task_manager/team_project_update.html"
    pk_url_kwarg = "pk_project"

    def get_success_url(self):
        team_name = get_slugify_team_name(self.request)["team_name"]
        return reverse(
            "task_manager:team_projects_list", kwargs={"team_name": team_name}
        )


class DeleteProjectView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    template_name = "task_manager/team_project_delete.html"
    pk_url_kwarg = "pk_project"

    def get_success_url(self):
        team_name = get_slugify_team_name(self.request)["team_name"]
        return reverse(
            "task_manager:team_projects_list", kwargs={"team_name": team_name}
        )


class CreateTaskView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "task_manager/create_project_task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_id"] = self.kwargs["pk_project"]
        return context

    def get_success_url(self):
        team_name = get_slugify_team_name(self.request)["team_name"]
        project_pk = self.kwargs["pk_project"]
        return reverse(
            "task_manager:team_project_tasks_list",
            kwargs={"team_name": team_name, "pk_project": project_pk},
        )

    def form_valid(self, form):
        form.instance.project = Project.objects.get(pk=self.kwargs["pk_project"])
        return super().form_valid(form)


class UpdateTaskView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "task_manager/team_project_task_update.html"
    pk_url_kwarg = "pk_task"

    def get_success_url(self):
        team_name = get_slugify_team_name(self.request)["team_name"]
        project_pk = self.kwargs["pk_project"]
        return reverse(
            "task_manager:team_project_tasks_list",
            kwargs={"team_name": team_name, "pk_project": project_pk},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team_members"] = Task.objects.get(
            pk=self.kwargs["pk_task"]
        ).project.team.worker_set.all()
        return context


class DeleteTaskView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task_manager/team_project_task_delete.html"
    pk_url_kwarg = "pk_task"

    def get_success_url(self):
        team_name = get_slugify_team_name(self.request)["team_name"]
        project_pk = self.kwargs["pk_project"]
        return reverse(
            "task_manager:team_project_tasks_list",
            kwargs={"team_name": team_name, "pk_project": project_pk},
        )


class InboxListView(LoginRequiredMixin, generic.ListView):
    model = MessageNew
    template_name = "task_manager/inbox.html"
    context_object_name = "messages"
    paginate_by = 10

    def get_queryset(self):
        queryset = MessageNew.objects.filter(
            to_worker=self.request.user.id, is_archieve=False
        )
        read_status = self.request.GET.get("status")
        search = self.request.GET.get("search")

        if read_status == "readed":
            queryset = queryset.filter(is_read=True)
        if read_status == "unread":
            queryset = queryset.filter(is_read=False)
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["read_status"] = self.request.GET.get("read_status", "all")
        context["sort_date"] = self.request.GET.get("sort_date", "none")
        return context

    def get_success_url(self):
        team_name = get_slugify_team_name(self.request)["team_name"]
        return reverse_lazy("task_manager:inbox", kwargs={"team_name": team_name})

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        message_ids = request.POST.getlist("message_ids[]")

        if action == "archive":
            MessageNew.objects.filter(
                id__in=message_ids, to_worker=request.user.id
            ).update(is_archieve=True)
        elif action == "delete":
            MessageNew.objects.filter(
                id__in=message_ids, to_worker=request.user.id
            ).delete()

        return redirect(self.get_success_url())


class MessageCreateView(LoginRequiredMixin, generic.CreateView):
    model = MessageNew
    fields = ("to_worker", "title", "content")
    template_name = "task_manager/create_message.html"

    def get_success_url(self):
        team_name = get_slugify_team_name(self.request)["team_name"]
        return reverse_lazy("task_manager:inbox", kwargs={"team_name": team_name})

    def form_valid(self, form):
        form.instance.from_worker = self.request.user
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, generic.DetailView, generic.edit.FormMixin):
    model = MessageNew
    template_name = "task_manager/message_detail.html"
    context_object_name = "message"
    pk_url_kwarg = "pk_message"
    form_class = ReplyMassageForm

    def get_object(self):
        self.context = MessageNew.objects.get(pk=self.kwargs["pk_message"])
        self.context.is_read = True
        self.context.save()
        return self.context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {"request": self.request, "to_worker": self.get_queryset()[0].from_worker}
        )
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

    def get_success_url(self):
        team_name = get_slugify_team_name(self.request)["team_name"]
        return reverse_lazy("task_manager:inbox", kwargs={"team_name": team_name})
