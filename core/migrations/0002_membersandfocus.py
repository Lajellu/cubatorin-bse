# Generated by Django 5.0.6 on 2025-06-26 01:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembersAndFocus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('high_level_problem', models.TextField()),
                ('mem1_name', models.TextField()),
                ('mem1_interest', models.TextField()),
                ('mem1_prob1', models.TextField()),
                ('mem1_prob2', models.TextField()),
                ('mem1_prob3', models.TextField()),
                ('mem1_prob4', models.TextField()),
                ('mem1_prob5', models.TextField()),
                ('mem2_name', models.TextField()),
                ('mem2_interest', models.TextField()),
                ('mem2_prob1', models.TextField()),
                ('mem2_prob2', models.TextField()),
                ('mem2_prob3', models.TextField()),
                ('mem2_prob4', models.TextField()),
                ('mem2_prob5', models.TextField()),
                ('mem3_name', models.TextField()),
                ('mem3_interest', models.TextField()),
                ('mem3_prob1', models.TextField()),
                ('mem3_prob2', models.TextField()),
                ('mem3_prob3', models.TextField()),
                ('mem3_prob4', models.TextField()),
                ('mem3_prob5', models.TextField()),
                ('mem4_name', models.TextField()),
                ('mem4_interest', models.TextField()),
                ('mem4_prob1', models.TextField()),
                ('mem4_prob2', models.TextField()),
                ('mem4_prob3', models.TextField()),
                ('mem4_prob4', models.TextField()),
                ('mem4_prob5', models.TextField()),
                ('mem5_name', models.TextField()),
                ('mem5_interest', models.TextField()),
                ('mem5_prob1', models.TextField()),
                ('mem5_prob2', models.TextField()),
                ('mem5_prob3', models.TextField()),
                ('mem5_prob4', models.TextField()),
                ('mem5_prob5', models.TextField()),
                ('fa1_prob1', models.TextField()),
                ('fa1_prob2', models.TextField()),
                ('fa1_prob3', models.TextField()),
                ('fa1_prob4', models.TextField()),
                ('fa1_prob5', models.TextField()),
                ('fa1_prob6', models.TextField()),
                ('fa1_prob7', models.TextField()),
                ('fa1_prob8', models.TextField()),
                ('fa1_prob9', models.TextField()),
                ('fa1_prob10', models.TextField()),
                ('fa2_prob1', models.TextField()),
                ('fa2_prob2', models.TextField()),
                ('fa2_prob3', models.TextField()),
                ('fa2_prob4', models.TextField()),
                ('fa2_prob5', models.TextField()),
                ('fa2_prob6', models.TextField()),
                ('fa2_prob7', models.TextField()),
                ('fa2_prob8', models.TextField()),
                ('fa2_prob9', models.TextField()),
                ('fa2_prob10', models.TextField()),
                ('fa3_prob1', models.TextField()),
                ('fa3_prob2', models.TextField()),
                ('fa3_prob3', models.TextField()),
                ('fa3_prob4', models.TextField()),
                ('fa3_prob5', models.TextField()),
                ('fa3_prob6', models.TextField()),
                ('fa3_prob7', models.TextField()),
                ('fa3_prob8', models.TextField()),
                ('fa3_prob9', models.TextField()),
                ('fa3_prob10', models.TextField()),
                ('fa4_prob1', models.TextField()),
                ('fa4_prob2', models.TextField()),
                ('fa4_prob3', models.TextField()),
                ('fa4_prob4', models.TextField()),
                ('fa4_prob5', models.TextField()),
                ('fa4_prob6', models.TextField()),
                ('fa4_prob7', models.TextField()),
                ('fa4_prob8', models.TextField()),
                ('fa4_prob9', models.TextField()),
                ('fa4_prob10', models.TextField()),
                ('fa5_prob1', models.TextField()),
                ('fa5_prob2', models.TextField()),
                ('fa5_prob3', models.TextField()),
                ('fa5_prob4', models.TextField()),
                ('fa5_prob5', models.TextField()),
                ('fa5_prob6', models.TextField()),
                ('fa5_prob7', models.TextField()),
                ('fa5_prob8', models.TextField()),
                ('fa5_prob9', models.TextField()),
                ('fa5_prob10', models.TextField()),
                ('fa6_prob1', models.TextField()),
                ('fa6_prob2', models.TextField()),
                ('fa6_prob3', models.TextField()),
                ('fa6_prob4', models.TextField()),
                ('fa6_prob5', models.TextField()),
                ('fa6_prob6', models.TextField()),
                ('fa6_prob7', models.TextField()),
                ('fa6_prob8', models.TextField()),
                ('fa6_prob9', models.TextField()),
                ('fa6_prob10', models.TextField()),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.team')),
            ],
        ),
    ]
