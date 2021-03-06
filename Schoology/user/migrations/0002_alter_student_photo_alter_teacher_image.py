# Generated by Django 4.0.2 on 2022-04-21 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(blank=True, default='student/picture1.jpg', null=True, upload_to='student/'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, default='teacher/default.png', null=True, upload_to='teacher/'),
        ),
    ]
