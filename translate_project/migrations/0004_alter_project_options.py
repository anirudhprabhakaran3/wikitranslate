# Generated by Django 4.0.1 on 2022-01-21 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('translate_project', '0003_sentence'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': [('can_appoint_translator', 'Can appoint translator')]},
        ),
    ]
