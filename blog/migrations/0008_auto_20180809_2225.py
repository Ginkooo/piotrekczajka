# Generated by Django 2.0.7 on 2018-08-09 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_newsletteraddresse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletteraddresse',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]