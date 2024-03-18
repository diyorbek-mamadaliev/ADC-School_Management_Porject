# Generated by Django 4.2.9 on 2024-02-02 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_corporatetax'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='last_payment',
            field=models.ForeignKey(blank=True, help_text='Last payment made by the student', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_payment_for_student', to='app.payments'),
        ),
    ]