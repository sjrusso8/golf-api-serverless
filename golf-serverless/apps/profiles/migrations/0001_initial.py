# Generated by Django 3.1.4 on 2020-12-23 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bio', models.TextField(blank=True, verbose_name='Personal Bio')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N', 'Prefer Not to Say')], default='N', max_length=50, verbose_name='Gender')),
                ('favorites', models.ManyToManyField(related_name='favorited_courses', to='api.Course')),
                ('follows', models.ManyToManyField(related_name='followed_by', to='profiles.Profile')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profile',
            },
        ),
    ]
