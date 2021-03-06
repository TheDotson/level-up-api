# Generated by Django 3.1.3 on 2020-12-02 01:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0004_auto_20201202_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventGamers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RenameField(
            model_name='game',
            old_name='gametype',
            new_name='game_type',
        ),
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', related_query_name='event', to='levelupapi.gamer'),
        ),
        migrations.AlterField(
            model_name='game',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='gamer',
            name='bio',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='gametype',
            name='label',
            field=models.CharField(max_length=55),
        ),
        migrations.DeleteModel(
            name='GamerEvent',
        ),
        migrations.AddField(
            model_name='eventgamers',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='levelupapi.event'),
        ),
        migrations.AddField(
            model_name='eventgamers',
            name='gamer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='levelupapi.gamer'),
        ),
    ]
