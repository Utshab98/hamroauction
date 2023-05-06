# Generated by Django 3.1.7 on 2021-10-04 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='tokens',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='valid_doc',
            field=models.ImageField(upload_to='verified_doc'),
        ),
    ]