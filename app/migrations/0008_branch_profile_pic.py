# Generated by Django 4.2.9 on 2024-02-19 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_branch_student_branch_alter_course_branch_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='media/profile_pic'),
        ),
    ]
