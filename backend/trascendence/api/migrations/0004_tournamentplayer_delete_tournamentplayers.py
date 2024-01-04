# Generated by Django 4.2.7 on 2024-01-04 13:55

from django.db import migrations, models
import django.db.models.deletion
import trascendence.api.models.SerializableModel
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_tournaments_tournamentplayers_tournamentinvitations_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournamentPlayer',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=36, primary_key=True, serialize=False)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_tournament_id', to='api.tournaments')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user', to='api.usermodel')),
            ],
            bases=(models.Model, trascendence.api.models.SerializableModel.SerializableModel),
        ),
        migrations.DeleteModel(
            name='TournamentPlayers',
        ),
    ]
