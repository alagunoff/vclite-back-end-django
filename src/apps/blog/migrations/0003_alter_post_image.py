# Generated by Django 4.1.1 on 2022-10-03 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_alter_post_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.TextField(max_length=900000),
        ),
    ]