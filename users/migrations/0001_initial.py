# Generated by Django 2.1.11 on 2020-02-03 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialism',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Category')),
                ('feedbacker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('linkedin', models.URLField(blank=True, verbose_name='LinkedIn')),
                ('url_link_1', models.URLField(blank=True, verbose_name='Personal Website Link 1')),
                ('url_link_2', models.URLField(blank=True, verbose_name='Personal Website Link 2')),
                ('url_link_3', models.URLField(blank=True, verbose_name='Personal Website Link 3')),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('premium_ends', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]