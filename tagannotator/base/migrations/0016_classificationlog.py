# Generated by Django 2.1.15 on 2020-02-05 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_auto_20200205_0958'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassificationLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logs', models.CharField(max_length=9999999)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Post')),
            ],
        ),
    ]