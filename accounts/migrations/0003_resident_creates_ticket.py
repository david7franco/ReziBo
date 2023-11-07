# Generated by Django 4.2.6 on 2023-11-03 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_taskid_task_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='resident_creates_ticket',
            fields=[
                ('resident_creates_ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('FK_resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.residentuser')),
                ('FK_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.task')),
            ],
        ),
    ]