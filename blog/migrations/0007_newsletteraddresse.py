# Generated by Django 2.0.7 on 2018-08-09 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20180723_0705'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsletterAddresse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('token', models.IntegerField()),
            ],
        ),
    ]
