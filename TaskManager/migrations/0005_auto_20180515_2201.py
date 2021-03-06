# Generated by Django 2.0.5 on 2018-05-15 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManager', '0004_auto_20180515_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('Высокий', 'Высокий'), ('Средний', 'Средний'), ('Низкий', 'Низкий')], default='Средний', max_length=10),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Выполнено', 'Выполнено'), ('Не выполнено', 'Не выполнено')], default='Не выполнено', max_length=10),
        ),
    ]
