# Generated by Django 3.1.2 on 2021-01-03 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('popcorn', '0003_CategoryExtension'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='num_vote_down',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='num_vote_up',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='vote_score',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]