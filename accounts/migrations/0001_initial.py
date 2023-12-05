# Generated by Django 4.2.6 on 2023-12-05 05:55

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="RaUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("floor", models.PositiveIntegerField()),
                ("ra_name", models.CharField(max_length=200)),
                ("room_number", models.PositiveIntegerField()),
                ("phone_number", models.CharField(blank=True, max_length=15)),
                ("ra_email", models.EmailField(default=None, max_length=254)),
                (
                    "image",
                    models.ImageField(null=True, upload_to="media/accounts/static"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ResidentUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("residentName", models.CharField(max_length=200)),
                ("floor", models.PositiveIntegerField()),
                ("resident_email", models.EmailField(default=None, max_length=254)),
                ("phone_number", models.CharField(blank=True, max_length=15)),
                ("room_number", models.PositiveIntegerField(default=0)),
                (
                    "image",
                    models.ImageField(null=True, upload_to="media/accounts/static"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TextEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=200)),
                ("floor", models.PositiveIntegerField(default=0)),
                ("description", models.TextField()),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (1, "To Do"),
                            (2, "In Progress"),
                            (3, "On Hold"),
                            (4, "Done"),
                        ],
                        default=1,
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(
                        choices=[(1, "Low"), (2, "Medium"), (3, "High")], default=1
                    ),
                ),
                (
                    "date_posted",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                ("file", models.FileField(blank=True, null=True, upload_to="")),
                (
                    "ra",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="ra_tasks",
                        to="accounts.rauser",
                    ),
                ),
                (
                    "resident",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="resident_tasks",
                        to="accounts.residentuser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comments",
            fields=[
                ("comment_id", models.AutoField(primary_key=True, serialize=False)),
                ("text", models.TextField()),
                ("date_posted", models.DateTimeField(default=datetime.datetime.now)),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "fk_task_comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="accounts.task",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ChatMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.TextField()),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                ("for_ras_only", models.BooleanField(default=False)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chat_messages",
                        to="accounts.task",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Annotations",
            fields=[
                ("annotate_id", models.AutoField(primary_key=True, serialize=False)),
                ("annotations", models.TextField()),
                ("date_posted", models.DateTimeField(default=datetime.datetime.now)),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "fk_task_annotations",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="annotations",
                        to="accounts.task",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AdminUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("admin_name", models.TextField()),
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
