import json

from django.contrib.auth.models import User
from django.db import models

class Competition(models.Model):
    name = models.TextField(blank=False, null=False, default='')

class Team(models.Model):
    name = models.TextField(blank=False, null=False, default='')
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    
from django.db import models

class MembersAndFocus(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    high_level_problem = models.TextField()

    # Member name and interest (up to 5 members), Member problem fields (up to 5 problems each)
    mem1_name = models.TextField()
    mem1_interest = models.TextField()
    mem1_prob1 = models.TextField()
    mem1_prob2 = models.TextField()
    mem1_prob3 = models.TextField()
    mem1_prob4 = models.TextField()
    mem1_prob5 = models.TextField()

    mem2_name = models.TextField()
    mem2_interest = models.TextField()
    mem2_prob1 = models.TextField()
    mem2_prob2 = models.TextField()
    mem2_prob3 = models.TextField()
    mem2_prob4 = models.TextField()
    mem2_prob5 = models.TextField()

    mem3_name = models.TextField()
    mem3_interest = models.TextField()
    mem3_prob1 = models.TextField()
    mem3_prob2 = models.TextField()
    mem3_prob3 = models.TextField()
    mem3_prob4 = models.TextField()
    mem3_prob5 = models.TextField()

    mem4_name = models.TextField()
    mem4_interest = models.TextField()
    mem4_prob1 = models.TextField()
    mem4_prob2 = models.TextField()
    mem4_prob3 = models.TextField()
    mem4_prob4 = models.TextField()
    mem4_prob5 = models.TextField()

    mem5_name = models.TextField()
    mem5_interest = models.TextField()
    mem5_prob1 = models.TextField()
    mem5_prob2 = models.TextField()
    mem5_prob3 = models.TextField()
    mem5_prob4 = models.TextField()
    mem5_prob5 = models.TextField()

    # Focus area fields (up to 6 focus areas)
    fa1_prob1 = models.TextField()
    fa1_prob2 = models.TextField()
    fa1_prob3 = models.TextField()
    fa1_prob4 = models.TextField()
    fa1_prob5 = models.TextField()
    fa1_prob6 = models.TextField()
    fa1_prob7 = models.TextField()
    fa1_prob8 = models.TextField()
    fa1_prob9 = models.TextField()
    fa1_prob10 = models.TextField()

    fa2_prob1 = models.TextField()
    fa2_prob2 = models.TextField()
    fa2_prob3 = models.TextField()
    fa2_prob4 = models.TextField()
    fa2_prob5 = models.TextField()
    fa2_prob6 = models.TextField()
    fa2_prob7 = models.TextField()
    fa2_prob8 = models.TextField()
    fa2_prob9 = models.TextField()
    fa2_prob10 = models.TextField()

    fa3_prob1 = models.TextField()
    fa3_prob2 = models.TextField()
    fa3_prob3 = models.TextField()
    fa3_prob4 = models.TextField()
    fa3_prob5 = models.TextField()
    fa3_prob6 = models.TextField()
    fa3_prob7 = models.TextField()
    fa3_prob8 = models.TextField()
    fa3_prob9 = models.TextField()
    fa3_prob10 = models.TextField()

    fa4_prob1 = models.TextField()
    fa4_prob2 = models.TextField()
    fa4_prob3 = models.TextField()
    fa4_prob4 = models.TextField()
    fa4_prob5 = models.TextField()
    fa4_prob6 = models.TextField()
    fa4_prob7 = models.TextField()
    fa4_prob8 = models.TextField()
    fa4_prob9 = models.TextField()
    fa4_prob10 = models.TextField()

    fa5_prob1 = models.TextField()
    fa5_prob2 = models.TextField()
    fa5_prob3 = models.TextField()
    fa5_prob4 = models.TextField()
    fa5_prob5 = models.TextField()
    fa5_prob6 = models.TextField()
    fa5_prob7 = models.TextField()
    fa5_prob8 = models.TextField()
    fa5_prob9 = models.TextField()
    fa5_prob10 = models.TextField()

    fa6_prob1 = models.TextField()
    fa6_prob2 = models.TextField()
    fa6_prob3 = models.TextField()
    fa6_prob4 = models.TextField()
    fa6_prob5 = models.TextField()
    fa6_prob6 = models.TextField()
    fa6_prob7 = models.TextField()
    fa6_prob8 = models.TextField()
    fa6_prob9 = models.TextField()
    fa6_prob10 = models.TextField()

    def __str__(self):
        return f"MembersAndFocus for {self.team}"
