# Generated by Django 4.1.1 on 2022-10-03 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.TextField(max_length=110),
        ),
    ]