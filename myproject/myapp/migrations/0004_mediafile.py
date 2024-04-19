# Generated by Django 5.0.1 on 2024-04-19 08:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0003_remove_video_audio"),
    ]

    operations = [
        migrations.CreateModel(
            name="MediaFile",
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
                ("video", models.FileField(upload_to="videos/")),
                ("audio", models.FileField(blank=True, null=True, upload_to="audios/")),
                ("eeg", models.FileField(blank=True, null=True, upload_to="eeg/")),
            ],
        ),
    ]