# Generated by Django 3.1.2 on 2020-11-01 21:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Measurment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=120)),
                ('short_name', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Moderator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('granted_on', models.DateTimeField(auto_now_add=True)),
                ('auth_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newsletter_signup', models.BinaryField()),
                ('blocked_on', models.DateTimeField()),
                ('blocked_till', models.DateTimeField()),
                ('deleted_on', models.DateTimeField()),
                ('auth_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('blocked_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blocked_users', to='popcorn.moderator')),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_users', to='popcorn.moderator')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('value', models.BinaryField()),
                ('voted_on', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='popcorn.user')),
                ('vote_target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=120)),
                ('content', models.TextField()),
                ('icon', models.ImageField(upload_to='')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('preparation_time', models.PositiveIntegerField()),
                ('servings_count', models.PositiveIntegerField()),
                ('difficulty', models.PositiveIntegerField()),
                ('hidden_on', models.DateTimeField()),
                ('deleted_on', models.DateTimeField()),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authored_recipes', to='popcorn.user')),
                ('categories', models.ManyToManyField(to='popcorn.Category')),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_recipes', to='popcorn.moderator')),
                ('hidden_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hidden_recipes', to='popcorn.moderator')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('count', models.PositiveIntegerField()),
                ('measurment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='popcorn.measurment')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='popcorn.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('deleted_on', models.DateTimeField()),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authored_comments', to='popcorn.user')),
                ('comment_parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments_deleted', to='popcorn.moderator')),
            ],
        ),
    ]
