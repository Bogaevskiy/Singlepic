# Generated by Django 2.2.3 on 2019-12-29 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0012_photo_blocked'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.CharField(default='', max_length=200),
        ),
    ]