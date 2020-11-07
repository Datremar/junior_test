# Generated by Django 3.1.2 on 2020-11-04 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='anonymous', max_length=64)),
                ('spent_money', models.IntegerField()),
                ('gem_name', models.CharField(default='none', max_length=32)),
                ('gems', models.IntegerField()),
                ('date', models.CharField(default='sometime', max_length=32)),
            ],
        ),
    ]
