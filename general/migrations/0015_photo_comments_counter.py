# Generated by Django 2.2.3 on 2020-03-16 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0014_auto_20200113_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='comments_counter',
            field=models.IntegerField(default=0),
        ),
    ]
