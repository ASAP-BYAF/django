# Generated by Django 4.1 on 2023-01-17 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conan_db_app', '0024_alter_case_complement_alter_case_kind_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='event_related_to',
            field=models.ManyToManyField(blank=True, null=True, to='conan_db_app.event'),
        ),
    ]
