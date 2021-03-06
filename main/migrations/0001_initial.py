# Generated by Django 2.1.11 on 2020-02-03 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackerCandidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application', models.CharField(default='', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackerComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedbacker_comments', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('maintext', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_started', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_completed', models.DateTimeField(default=django.utils.timezone.now)),
                ('time_limit', models.IntegerField(default=7)),
                ('reward', models.IntegerField(default=0)),
                ('feedbacker_comments', models.TextField(default='')),
                ('feedbacker_rated', models.IntegerField(default=False)),
                ('area', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.Area')),
                ('feedbackee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_feedbackee', to=settings.AUTH_USER_MODEL)),
                ('feedbacker', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='request_feedbacker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_completed', models.IntegerField(default=False)),
                ('feedback', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.FeedbackRequest')),
                ('feedbackee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='buyer', to=settings.AUTH_USER_MODEL)),
                ('feedbacker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('overall', models.IntegerField(default=0)),
                ('quality', models.IntegerField(default=0)),
                ('speed', models.IntegerField(default=0)),
                ('communication', models.IntegerField(default=0)),
                ('review', models.TextField(default='')),
                ('feedbackee', models.ForeignKey(on_delete=models.SET('Anonymous'), related_name='rating_feedbackee', to=settings.AUTH_USER_MODEL)),
                ('feedbacker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_feedbacker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Category')),
                ('feedback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.FeedbackRequest')),
            ],
        ),
        migrations.AddField(
            model_name='feedbackercandidate',
            name='feedback',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.FeedbackRequest'),
        ),
        migrations.AddField(
            model_name='feedbackercandidate',
            name='feedbacker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
