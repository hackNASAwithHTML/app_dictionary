# Generated by Django 3.0.8 on 2020-11-25 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_backend', '0008_inputvocabulary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputvocabulary',
            name='class_in_Vietnamese',
            field=models.CharField(choices=[('Tính từ', 'Tính từ'), ('Trạng từ', 'Trạng từ'), ('Giới từ', 'Giới từ'), ('Danh từ', 'Danh từ'), ('Đại từ', 'Đại từ'), ('Động từ', 'Động từ')], default='Động từ', max_length=254, null=True),
        ),
    ]
