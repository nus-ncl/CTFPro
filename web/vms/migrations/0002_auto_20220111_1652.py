# Generated by Django 3.2.7 on 2022-01-11 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='state',
            field=models.CharField(default=1, max_length=45),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='component',
            name='component_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
