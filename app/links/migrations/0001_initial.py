# Generated by Django 5.1.5 on 2025-02-05 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ShortURL',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('original', models.URLField(unique=True)),
                ('token', models.CharField(editable=False, max_length=10, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('click_count', models.BigIntegerField(default=0)),
            ],
        ),
    ]
