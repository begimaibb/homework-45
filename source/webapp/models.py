from django.db import models


# Create your models here.

class Task(models.Model):
    status_choices = [('new', 'New'), ('in_progress', 'In progress'), ('done', 'Done')]
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Name")
    description = models.TextField(max_length=100, null=True, blank=True, verbose_name="Description")
    status = models.CharField(max_length=50, choices=status_choices, default='1')
    date = models.DateField(max_length=50, null=True, blank=True, verbose_name="Date")


    def __str__(self):
        return f"{self.id}. {self.name}, {self.description} {self.status} {self.date}"

    class Meta:
        db_table = "tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

