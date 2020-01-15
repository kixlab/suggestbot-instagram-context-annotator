# Generated by Django 2.2.7 on 2020-01-14 15:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0005_auto_20200113_0518'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Session'),
        ),
        migrations.AddField(
            model_name='post',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Session'),
        ),
        migrations.AlterField(
            model_name='session',
            name='endtime',
            field=models.DateTimeField(blank=True, default=None),
        ),
        migrations.CreateModel(
            name='UsedPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='base.Post')),
                ('uploadedphoto', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='base.Photo')),
            ],
        ),
        migrations.CreateModel(
            name='InstaPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashed_post_url', models.CharField(max_length=200)),
                ('post', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='base.Post')),
            ],
        ),
        migrations.CreateModel(
            name='InstagramAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashed_account_id', models.CharField(max_length=200)),
                ('suspicous', models.BooleanField(default=False)),
                ('duplicated', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
