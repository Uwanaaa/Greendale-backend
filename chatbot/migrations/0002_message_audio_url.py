# Generated by Django 4.2.11 on 2025-03-25 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='audio_url',
            field=models.CharField(blank=True, default=None, max_length=80, null=True),
        ),
    ]
