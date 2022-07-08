from django.db import models


# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date updated")

    class Meta:
        abstract = True


class Status(BaseModel):
    status_name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Status")

    def __str__(self):
        return f"{self.id}. {self.status_name}"

    class Meta:
        db_table = "statuses"
        verbose_name = "Status"
        verbose_name_plural = "Statuses"


class Type(BaseModel):
    type_name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Type")

    def __str__(self):
        return f"{self.id}. {self.type_name}"

    class Meta:
        db_table = "types"
        verbose_name = "Type"
        verbose_name_plural = "Types"


class Task(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Name")
    description = models.TextField(max_length=100, null=True, blank=True, verbose_name="Description")
    status = models.ForeignKey("webapp.Status", on_delete=models.CASCADE, related_name='status')
    type = models.ForeignKey("webapp.Type", on_delete=models.CASCADE, related_name='type')

    def __str__(self):
        return f"{self.id}. {self.name}, {self.description} {self.status} {self.type}"

    class Meta:
        db_table = "tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"