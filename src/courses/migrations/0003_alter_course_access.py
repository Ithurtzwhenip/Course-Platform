# Generated by Django 5.1.6 on 2025-03-02 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_alter_course_access'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='access',
            field=models.CharField(choices=[('any', 'Anyone'), ('email', 'Email Required')], default='email', max_length=5),
        ),
    ]
