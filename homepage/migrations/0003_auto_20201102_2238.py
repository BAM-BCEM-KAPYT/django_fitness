# Generated by Django 3.1.1 on 2020-11-02 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_auto_20201102_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='homepage.group'),
        ),
    ]
