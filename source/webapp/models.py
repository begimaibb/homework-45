from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date updated")

    class Meta:
        abstract = True


class Status(BaseModel):
    status_name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Status")

    def __str__(self):
        return f"{self.status_name}"

    class Meta:
        db_table = "statuses"
        verbose_name = "Status"
        verbose_name_plural = "Statuses"


class Type(BaseModel):
    type_name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Type")

    def __str__(self):
        return f"{self.type_name}"

    class Meta:
        db_table = "types"
        verbose_name = "Type"
        verbose_name_plural = "Types"


class Project(models.Model):
    date_started = models.DateField(auto_now_add=False, null=False, blank=False, verbose_name="Date created")
    date_finished = models.DateField(auto_now_add=False, null=True, blank=True, verbose_name="Date finished")
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Name")
    description = models.TextField(max_length=100, null=True, blank=False, verbose_name="Description")
    user = models.ManyToManyField(get_user_model(), related_name="projects", blank=True)

    def __str__(self):
        return f"{self.id} {self.name}: {self.description} {self.user.username}"

    def get_absolute_url(self):
        return reverse("webapp:project_view", kwargs={"pk": self.pk})

    def upper(self):
        return self.title.upper()

    class Meta:
        db_table = "projects"
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class Task(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Name")
    description = models.TextField(max_length=100, null=True, blank=True, verbose_name="Description")
    status = models.ForeignKey("webapp.Status", on_delete=models.PROTECT, related_name='status')
    type = models.ManyToManyField("webapp.Type", related_name="tasks", blank=True)
    project = models.ForeignKey("webapp.Project", on_delete=models.CASCADE, related_name='project')

    def __str__(self):
        return f"{self.id}. {self.name}, {self.description} {self.status} {self.type}"

    def get_absolute_url(self):
        return reverse("webapp:task_view", kwargs={"pk": self.pk})

    class Meta:
        db_table = "tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

