# Generated by Django 5.2 on 2025-05-03 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_remove_article_sha256_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='sha256_hash',
            field=models.CharField(blank=True, db_index=True, max_length=64, null=True, unique=True),
        ),
    ]
