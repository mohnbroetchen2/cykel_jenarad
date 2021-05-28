# Generated by Django 3.1.2 on 2021-01-21 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bikesharing', '0047_auto_20210120_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoxiatrackerupdate',
            name='datetime',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='invoxiatrackerupdate',
            name='energy_level',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='invoxiatrackerupdate',
            name='precision',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]