import json

from django.contrib.auth.models import User
from django.db import models

class Competition(models.Model):
    name = models.TextField(blank=False, null=False, default='')

class Team(models.Model):
    name = models.TextField(blank=False, null=False, default='')
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    
class MembersAndFocus(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    high_level_problem = models.TextField(default="", blank=True)

    # Member name and interest (up to 5 members), Member problem fields (up to 5 problems each)
    mem1_name = models.TextField(default="", blank=True)
    mem1_interest = models.TextField(default="", blank=True)
    mem1_prob1 = models.TextField(default="", blank=True)
    mem1_prob2 = models.TextField(default="", blank=True)
    mem1_prob3 = models.TextField(default="", blank=True)
    mem1_prob4 = models.TextField(default="", blank=True)
    mem1_prob5 = models.TextField(default="", blank=True)

    mem2_name = models.TextField(default="", blank=True)
    mem2_interest = models.TextField(default="", blank=True)
    mem2_prob1 = models.TextField(default="", blank=True)
    mem2_prob2 = models.TextField(default="", blank=True)
    mem2_prob3 = models.TextField(default="", blank=True)
    mem2_prob4 = models.TextField(default="", blank=True)
    mem2_prob5 = models.TextField(default="", blank=True)

    mem3_name = models.TextField(default="", blank=True)
    mem3_interest = models.TextField(default="", blank=True)
    mem3_prob1 = models.TextField(default="", blank=True)
    mem3_prob2 = models.TextField(default="", blank=True)
    mem3_prob3 = models.TextField(default="", blank=True)
    mem3_prob4 = models.TextField(default="", blank=True)
    mem3_prob5 = models.TextField(default="", blank=True)

    mem4_name = models.TextField(default="", blank=True)
    mem4_interest = models.TextField(default="", blank=True)
    mem4_prob1 = models.TextField(default="", blank=True)
    mem4_prob2 = models.TextField(default="", blank=True)
    mem4_prob3 = models.TextField(default="", blank=True)
    mem4_prob4 = models.TextField(default="", blank=True)
    mem4_prob5 = models.TextField(default="", blank=True)

    mem5_name = models.TextField(default="", blank=True)
    mem5_interest = models.TextField(default="", blank=True)
    mem5_prob1 = models.TextField(default="", blank=True)
    mem5_prob2 = models.TextField(default="", blank=True)
    mem5_prob3 = models.TextField(default="", blank=True)
    mem5_prob4 = models.TextField(default="", blank=True)
    mem5_prob5 = models.TextField(default="", blank=True)

    # Focus area fields (up to 6 focus areas)
    fa1_prob1 = models.TextField(default="", blank=True)
    fa1_prob2 = models.TextField(default="", blank=True)
    fa1_prob3 = models.TextField(default="", blank=True)
    fa1_prob4 = models.TextField(default="", blank=True)
    fa1_prob5 = models.TextField(default="", blank=True)
    fa1_prob6 = models.TextField(default="", blank=True)
    fa1_prob7 = models.TextField(default="", blank=True)
    fa1_prob8 = models.TextField(default="", blank=True)
    fa1_prob9 = models.TextField(default="", blank=True)
    fa1_prob10 = models.TextField(default="", blank=True)

    fa2_prob1 = models.TextField(default="", blank=True)
    fa2_prob2 = models.TextField(default="", blank=True)
    fa2_prob3 = models.TextField(default="", blank=True)
    fa2_prob4 = models.TextField(default="", blank=True)
    fa2_prob5 = models.TextField(default="", blank=True)
    fa2_prob6 = models.TextField(default="", blank=True)
    fa2_prob7 = models.TextField(default="", blank=True)
    fa2_prob8 = models.TextField(default="", blank=True)
    fa2_prob9 = models.TextField(default="", blank=True)
    fa2_prob10 = models.TextField(default="", blank=True)

    fa3_prob1 = models.TextField(default="", blank=True)
    fa3_prob2 = models.TextField(default="", blank=True)
    fa3_prob3 = models.TextField(default="", blank=True)
    fa3_prob4 = models.TextField(default="", blank=True)
    fa3_prob5 = models.TextField(default="", blank=True)
    fa3_prob6 = models.TextField(default="", blank=True)
    fa3_prob7 = models.TextField(default="", blank=True)
    fa3_prob8 = models.TextField(default="", blank=True)
    fa3_prob9 = models.TextField(default="", blank=True)
    fa3_prob10 = models.TextField(default="", blank=True)

    fa4_prob1 = models.TextField(default="", blank=True)
    fa4_prob2 = models.TextField(default="", blank=True)
    fa4_prob3 = models.TextField(default="", blank=True)
    fa4_prob4 = models.TextField(default="", blank=True)
    fa4_prob5 = models.TextField(default="", blank=True)
    fa4_prob6 = models.TextField(default="", blank=True)
    fa4_prob7 = models.TextField(default="", blank=True)
    fa4_prob8 = models.TextField(default="", blank=True)
    fa4_prob9 = models.TextField(default="", blank=True)
    fa4_prob10 = models.TextField(default="", blank=True)

    fa5_prob1 = models.TextField(default="", blank=True)
    fa5_prob2 = models.TextField(default="", blank=True)
    fa5_prob3 = models.TextField(default="", blank=True)
    fa5_prob4 = models.TextField(default="", blank=True)
    fa5_prob5 = models.TextField(default="", blank=True)
    fa5_prob6 = models.TextField(default="", blank=True)
    fa5_prob7 = models.TextField(default="", blank=True)
    fa5_prob8 = models.TextField(default="", blank=True)
    fa5_prob9 = models.TextField(default="", blank=True)
    fa5_prob10 = models.TextField(default="", blank=True)

    fa6_prob1 = models.TextField(default="", blank=True)
    fa6_prob2 = models.TextField(default="", blank=True)
    fa6_prob3 = models.TextField(default="", blank=True)
    fa6_prob4 = models.TextField(default="", blank=True)
    fa6_prob5 = models.TextField(default="", blank=True)
    fa6_prob6 = models.TextField(default="", blank=True)
    fa6_prob7 = models.TextField(default="", blank=True)
    fa6_prob8 = models.TextField(default="", blank=True)
    fa6_prob9 = models.TextField(default="", blank=True)
    fa6_prob10 = models.TextField(default="", blank=True)

    def __str__(self):
        return f"MembersAndFocus for {self.team}"

class OpportunityDiscovery(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    problem_to_investigate = models.TextField(default="", blank=True)
    
    prob1 = models.TextField(default="", blank=True)
    causes1 = models.TextField(default="", blank=True)
    assumptions1 = models.TextField(default="", blank=True)
    difficulty1 = models.TextField(default="", blank=True)
    impact1 = models.TextField(default="", blank=True)

    prob2 = models.TextField(default="", blank=True)
    causes2 = models.TextField(default="", blank=True)
    assumptions2 = models.TextField(default="", blank=True)
    difficulty2 = models.TextField(default="", blank=True)
    impact2 = models.TextField(default="", blank=True)

    prob3 = models.TextField(default="", blank=True)
    causes3 = models.TextField(default="", blank=True)
    assumptions3 = models.TextField(default="", blank=True)
    difficulty3 = models.TextField(default="", blank=True)
    impact3 = models.TextField(default="", blank=True)

    prob4 = models.TextField(default="", blank=True)
    causes4 = models.TextField(default="", blank=True)
    assumptions4 = models.TextField(default="", blank=True)
    difficulty4 = models.TextField(default="", blank=True)
    impact4 = models.TextField(default="", blank=True)

    prob5 = models.TextField(default="", blank=True)
    causes5 = models.TextField(default="", blank=True)
    assumptions5 = models.TextField(default="", blank=True)
    difficulty5 = models.TextField(default="", blank=True)
    impact5 = models.TextField(default="", blank=True)

    prob6 = models.TextField(default="", blank=True)
    causes6 = models.TextField(default="", blank=True)
    assumptions6 = models.TextField(default="", blank=True)
    difficulty6 = models.TextField(default="", blank=True)
    impact6 = models.TextField(default="", blank=True)    
        
    
class UserNeed(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    first_customer = models.TextField(default="", blank=True)

    users_and_problem1 = models.TextField(default="", blank=True)
    functional_need1 = models.TextField(default="", blank=True)
    emotional_need1 = models.TextField(default="", blank=True)
    severity1 = models.TextField(default="", blank=True)
    existing_solution1 = models.TextField(default="", blank=True)
    ranking1 = models.TextField(default="", blank=True)
    
    users_and_problem2 = models.TextField(default="", blank=True)
    functional_need2 = models.TextField(default="", blank=True)
    emotional_need2 = models.TextField(default="", blank=True)
    severity2 = models.TextField(default="", blank=True)
    existing_solution2 = models.TextField(default="", blank=True)
    ranking2 = models.TextField(default="", blank=True)

    users_and_problem3 = models.TextField(default="", blank=True)
    functional_need3 = models.TextField(default="", blank=True)
    emotional_need3 = models.TextField(default="", blank=True)
    severity3 = models.TextField(default="", blank=True)
    existing_solution3 = models.TextField(default="", blank=True)
    ranking3 = models.TextField(default="", blank=True)

    users_and_problem4 = models.TextField(default="", blank=True)
    functional_need4 = models.TextField(default="", blank=True)
    emotional_need4 = models.TextField(default="", blank=True)
    severity4 = models.TextField(default="", blank=True)
    existing_solution4 = models.TextField(default="", blank=True)
    ranking4 = models.TextField(default="", blank=True)
    
class RootCause(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE)

    present_state1 = models.TextField(default="", blank=True)
    desired_state1 = models.TextField(default="", blank=True)
    research1 = models.TextField(default="Why are labs necessary? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\n", blank=True)
    root_cause1 = models.TextField(default="", blank=True)
    
    present_state2 = models.TextField(default="", blank=True)
    desired_state2 = models.TextField(default="", blank=True)
    research2 = models.TextField(default="Why are labs necessary? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\n", blank=True)
    root_cause2 = models.TextField(default="", blank=True)

    present_state3 = models.TextField(default="", blank=True)
    desired_state3 = models.TextField(default="", blank=True)
    research3 = models.TextField(default="Why are labs necessary? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\n", blank=True)
    root_cause3 = models.TextField(default="", blank=True)

    present_state4 = models.TextField(default="", blank=True)
    desired_state4 = models.TextField(default="", blank=True)
    research4 = models.TextField(default="Why are labs necessary? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\n", blank=True)
    root_cause4 = models.TextField(default="", blank=True)
    
    present_state5 = models.TextField(default="", blank=True)
    desired_state5 = models.TextField(default="", blank=True)
    research5 = models.TextField(default="Why are labs necessary? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\n", blank=True)
    root_cause5 = models.TextField(default="", blank=True)

class HowMightWe(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    how_might_we = models.TextField(default="", blank=True)
    
    root_cause1 = models.TextField(default="", blank=True)
    hmw1 = models.TextField(default="How might we...", blank=True)
    rank1 = models.TextField(default="", blank=True)

    root_cause2 = models.TextField(default="", blank=True)
    hmw2 = models.TextField(default="How might we...", blank=True)
    rank2 = models.TextField(default="", blank=True)

    root_cause3 = models.TextField(default="", blank=True)
    hmw3 = models.TextField(default="How might we...", blank=True)
    rank3 = models.TextField(default="", blank=True)

    root_cause4 = models.TextField(default="", blank=True)
    hmw4 = models.TextField(default="How might we...", blank=True)
    rank4 = models.TextField(default="", blank=True)

    root_cause5 = models.TextField(default="", blank=True)
    hmw5 = models.TextField(default="How might we...", blank=True)
    rank5 = models.TextField(default="", blank=True)
    
    top_hmw1 = models.TextField(default="How might we...", blank=True)
    top_hmw2 = models.TextField(default="How might we...", blank=True)
    top_hmw3 = models.TextField(default="How might we...", blank=True)

class SolutionIdeation(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE)

    eco_approach1 = models.TextField(default="", blank=True)
    eco_approach2 = models.TextField(default="", blank=True)
    eco_approach3 = models.TextField(default="", blank=True)
    eco_approach4 = models.TextField(default="", blank=True)
    eco_approach5 = models.TextField(default="", blank=True)
    eco_approach6 = models.TextField(default="", blank=True)
    eco_approach7 = models.TextField(default="", blank=True)
    
    tech_approach1 = models.TextField(default="", blank=True)
    tech_approach2 = models.TextField(default="", blank=True)
    tech_approach3 = models.TextField(default="", blank=True)
    tech_approach4 = models.TextField(default="", blank=True)
    tech_approach5 = models.TextField(default="", blank=True)
    tech_approach6 = models.TextField(default="", blank=True)
    tech_approach7 = models.TextField(default="", blank=True)
    
    behave_approach1 = models.TextField(default="", blank=True)
    behave_approach2 = models.TextField(default="", blank=True)
    behave_approach3 = models.TextField(default="", blank=True)
    behave_approach4 = models.TextField(default="", blank=True)
    behave_approach5 = models.TextField(default="", blank=True)
    behave_approach6 = models.TextField(default="", blank=True)
    behave_approach7 = models.TextField(default="", blank=True)
    
    # sg = solution group (4 total)
    # ag = approach group (3 for each sg)
    # a = approach (5 for each ag)
    sg1 = models.TextField(default="", blank=True)
    sg1_ag1_a1 = models.TextField(default="", blank=True)
    sg1_ag1_a2 = models.TextField(default="", blank=True)
    sg1_ag1_a3 = models.TextField(default="", blank=True)
    sg1_ag1_a4 = models.TextField(default="", blank=True)
    sg1_ag1_a5 = models.TextField(default="", blank=True)
    sg1_ag1_solution = models.TextField(default="", blank=True)

    sg1_ag2_a1 = models.TextField(default="", blank=True)
    sg1_ag2_a2 = models.TextField(default="", blank=True)
    sg1_ag2_a3 = models.TextField(default="", blank=True)
    sg1_ag2_a4 = models.TextField(default="", blank=True)
    sg1_ag2_a5 = models.TextField(default="", blank=True)
    sg1_ag2_solution = models.TextField(default="", blank=True)

    sg1_ag3_a1 = models.TextField(default="", blank=True)
    sg1_ag3_a2 = models.TextField(default="", blank=True)
    sg1_ag3_a3 = models.TextField(default="", blank=True)
    sg1_ag3_a4 = models.TextField(default="", blank=True)
    sg1_ag3_a5 = models.TextField(default="", blank=True)
    sg1_ag3_solution = models.TextField(default="", blank=True)

    sg2 = models.TextField(default="", blank=True)
    sg2_ag1_a1 = models.TextField(default="", blank=True)
    sg2_ag1_a2 = models.TextField(default="", blank=True)
    sg2_ag1_a3 = models.TextField(default="", blank=True)
    sg2_ag1_a4 = models.TextField(default="", blank=True)
    sg2_ag1_a5 = models.TextField(default="", blank=True)
    sg2_ag1_solution = models.TextField(default="", blank=True)

    sg2_ag2_a1 = models.TextField(default="", blank=True)
    sg2_ag2_a2 = models.TextField(default="", blank=True)
    sg2_ag2_a3 = models.TextField(default="", blank=True)
    sg2_ag2_a4 = models.TextField(default="", blank=True)
    sg2_ag2_a5 = models.TextField(default="", blank=True)
    sg2_ag2_solution = models.TextField(default="", blank=True)

    sg2_ag3_a1 = models.TextField(default="", blank=True)
    sg2_ag3_a2 = models.TextField(default="", blank=True)
    sg2_ag3_a3 = models.TextField(default="", blank=True)
    sg2_ag3_a4 = models.TextField(default="", blank=True)
    sg2_ag3_a5 = models.TextField(default="", blank=True)
    sg2_ag3_solution = models.TextField(default="", blank=True)

    sg3 = models.TextField(default="", blank=True)
    sg3_ag1_a1 = models.TextField(default="", blank=True)
    sg3_ag1_a2 = models.TextField(default="", blank=True)
    sg3_ag1_a3 = models.TextField(default="", blank=True)
    sg3_ag1_a4 = models.TextField(default="", blank=True)
    sg3_ag1_a5 = models.TextField(default="", blank=True)
    sg3_ag1_solution = models.TextField(default="", blank=True)

    sg3_ag2_a1 = models.TextField(default="", blank=True)
    sg3_ag2_a2 = models.TextField(default="", blank=True)
    sg3_ag2_a3 = models.TextField(default="", blank=True)
    sg3_ag2_a4 = models.TextField(default="", blank=True)
    sg3_ag2_a5 = models.TextField(default="", blank=True)
    sg3_ag2_solution = models.TextField(default="", blank=True)

    sg3_ag3_a1 = models.TextField(default="", blank=True)
    sg3_ag3_a2 = models.TextField(default="", blank=True)
    sg3_ag3_a3 = models.TextField(default="", blank=True)
    sg3_ag3_a4 = models.TextField(default="", blank=True)
    sg3_ag3_a5 = models.TextField(default="", blank=True)
    sg3_ag3_solution = models.TextField(default="", blank=True)

    sg4 = models.TextField(default="", blank=True)
    sg4_ag1_a1 = models.TextField(default="", blank=True)
    sg4_ag1_a2 = models.TextField(default="", blank=True)
    sg4_ag1_a3 = models.TextField(default="", blank=True)
    sg4_ag1_a4 = models.TextField(default="", blank=True)
    sg4_ag1_a5 = models.TextField(default="", blank=True)
    sg4_ag1_solution = models.TextField(default="", blank=True)

    sg4_ag2_a1 = models.TextField(default="", blank=True)
    sg4_ag2_a2 = models.TextField(default="", blank=True)
    sg4_ag2_a3 = models.TextField(default="", blank=True)
    sg4_ag2_a4 = models.TextField(default="", blank=True)
    sg4_ag2_a5 = models.TextField(default="", blank=True)
    sg4_ag2_solution = models.TextField(default="", blank=True)

    sg4_ag3_a1 = models.TextField(default="", blank=True)
    sg4_ag3_a2 = models.TextField(default="", blank=True)
    sg4_ag3_a3 = models.TextField(default="", blank=True)
    sg4_ag3_a4 = models.TextField(default="", blank=True)
    sg4_ag3_a5 = models.TextField(default="", blank=True)
    sg4_ag3_solution = models.TextField(default="", blank=True)

    
    