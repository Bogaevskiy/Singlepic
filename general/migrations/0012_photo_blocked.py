# Generated by Django 2.2.3 on 2019-12-07 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0011_comment_blocked'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='blocked',
            field=models.BooleanField(default=False),
        ),
    ]
