# Generated by Django 3.1.2 on 2021-01-20 22:21

from django.db import migrations, models
import popcorn.models


class Migration(migrations.Migration):

    dependencies = [
        ('popcorn', '0004_VoteableComments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='icon',
            field=models.ImageField(max_length=250, upload_to='recipes_icons', validators=[popcorn.models.validate_recipe_icon]),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(blank=True, max_length=130, null=True),
        ),
    ]
