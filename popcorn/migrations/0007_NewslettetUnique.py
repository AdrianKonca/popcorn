# Generated by Django 3.1.2 on 2021-01-24 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('popcorn', '0006_Newsletter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newslettersignup',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
