# Generated by Django 5.1.6 on 2025-03-03 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_rename_my_related_obj_lesson_course_lesson_thumbnail_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='lesson',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
