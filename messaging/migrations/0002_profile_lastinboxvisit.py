# Generated by Django 4.0.1 on 2022-04-27 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='lastInboxVisit',
            field=models.DateField(null=True),
        ),
    ]
