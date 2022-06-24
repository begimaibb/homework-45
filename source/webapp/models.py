from django.db import models


# Create your models here.

class Task(models.Model):
    status_choices = [('new', 'New'), ('in_progress', 'In progress'), ('done', 'Done')]
    date_input_formats = ('%dd-%mm-%YY', '%YY-%mm-%dd')
    description = models.TextField(max_length=50, null=False, blank=False, verbose_name="Description")
    status = models.CharField(max_length=20, choices=status_choices, default='1')
    date = models.TextField(max_length=10, null=False, blank=False, verbose_name="Date")


    def __str__(self):
        return f"{self.id}. {self.description} {self.status} {self.date}"

    class Meta:
        db_table = "tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

