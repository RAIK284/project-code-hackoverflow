# Generated by Django 4.0.1 on 2022-03-10 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0003_remove_conversation_members_usergroup_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='name',
            field=models.TextField(default='Conversation', max_length=400),
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='name',
            field=models.TextField(max_length=400),
        ),
    ]
