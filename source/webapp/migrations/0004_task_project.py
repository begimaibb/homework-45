# Generated by Django 4.0.5 on 2022-07-26 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_project_alter_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='project', to='webapp.project'),
        ),
    ]