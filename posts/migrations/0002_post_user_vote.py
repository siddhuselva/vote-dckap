# Generated by Django 4.0.5 on 2022-06-20 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user_vote',
            field=models.ManyToManyField(blank=True, default=None, related_name='user_vote', to='posts.user'),
        ),
    ]
