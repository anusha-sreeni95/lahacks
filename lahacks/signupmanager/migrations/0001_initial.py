# Generated by Django 2.2.10 on 2020-03-28 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('full_name', models.TextField()),
                ('email_address', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('password', models.TextField()),
            ],
        ),
    ]