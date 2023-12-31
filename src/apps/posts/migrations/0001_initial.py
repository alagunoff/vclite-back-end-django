# Generated by Django 4.1.1 on 2022-11-16 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authors', '0001_initial'),
        ('categories', '0001_initial'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('image', models.CharField(default='data:image/png;base64,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', max_length=900000)),
                ('is_draft', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.category')),
                ('tags', models.ManyToManyField(related_name='posts', to='tags.tag')),
            ],
            options={
                'db_table': 'posts',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PostExtraImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=900000)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extra_images', to='posts.post')),
            ],
            options={
                'db_table': 'post_extra_images',
                'ordering': ['id'],
            },
        ),
    ]
