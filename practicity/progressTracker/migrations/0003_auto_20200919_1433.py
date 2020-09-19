# Generated by Django 3.1.1 on 2020-09-19 12:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('progressTracker', '0002_auto_20200919_1045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='practicesession',
            name='exercise',
        ),
        migrations.AddField(
            model_name='exercise',
            name='practice_session',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='progressTracker.practicesession'),
            preserve_default=False,
        ),
    ]