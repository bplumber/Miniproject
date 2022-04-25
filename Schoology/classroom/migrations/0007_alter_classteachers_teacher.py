# Generated by Django 4.0.2 on 2022-04-23 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_student_photo_links'),
        ('classroom', '0006_alter_assignment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classteachers',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.teacher'),
        ),
    ]
