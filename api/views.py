import threading
import logging
import requests
import ssl
import certifi

from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import FieldDoesNotExist
from core.models import MembersAndFocus
from ai import ai


@api_view(['POST'])
def save_field(request):
    print("Received a request to /api/save_field")

    data = request.data

    table = data.get('table')
    field = data.get('field')
    value = data.get('value')
    team_id = data.get('team_id')

    if not table or not field or value is None or not team_id:
        return Response(
            {"error": "Missing one or more required fields: 'table', 'field', 'value', or 'team_id'."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        model = apps.get_model("core", table)  # Replace 'core' with your actual app label
        Team = apps.get_model("core", "Team")
    except LookupError as e:
        return Response({"error": f"Model lookup error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    # Validate team_id exists
    try:
        team_instance = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return Response({"error": f"Team with id={team_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

    # Check that the model has a foreign key to Team
    fk_fields = [
        f for f in model._meta.fields
        if f.is_relation and f.related_model == Team
    ]

    if not fk_fields:
        return Response({"error": f"Model '{table}' has no ForeignKey to Team."}, status=status.HTTP_400_BAD_REQUEST)

    # Use the first ForeignKey to Team as the link field
    team_fk_field = fk_fields[0].name

    # Find instance using team foreign key
    filter_kwargs = {team_fk_field: team_id}
    instance = model.objects.filter(**filter_kwargs).first()

    # if no row exists, create it and set its team
    if not instance:
        instance = model(team=team_instance)

    try:
        instance._meta.get_field(field)
    except FieldDoesNotExist:
        return Response({"error": f"Field {field} doesn't exist in {table}"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Dynamically assign the field
    setattr(instance, field, value)

    try:
        instance.save()
    except Exception as e:
        return Response({"error": f"Failed to save: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "message": "Value saved successfully.",
        "model": table,
        "team_id": team_id,
        "field": field,
        "value": value,
        "object_id": instance.id
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def suggest_focus_areas(request):
    print("Received a request to /api/suggest_focus_areas/")

    data = request.data
    team_id = data.get('team_id')
    print(team_id)
    if not team_id:
        return Response({"error": "Missing team_id"}, status=status.HTTP_400_BAD_REQUEST)

    members_and_focus = MembersAndFocus.objects.filter(team_id=team_id).first()

    if not members_and_focus:
        return Response({
            "error": f"No MembersAndFocus entry found for team_id={team_id}"
        }, status=status.HTTP_404_NOT_FOUND)

    # want to genereate: 
    #   John is interested in Biotech and wants to solve these problems: p1, p2, p3, ...
    #   Jill is ... etc
    output_lines = []

    for i in range(1, 6):  # mem1 to mem5
        name = getattr(members_and_focus, f"mem{i}_name", "").strip()
        interest = getattr(members_and_focus, f"mem{i}_interest", "").strip()

        # Skip if no name and no interest
        if not name and not interest:
            continue

        # Get non-empty problems
        problems = []
        for j in range(1, 6):  # prob1 to prob5
            prob_value = getattr(members_and_focus, f"mem{i}_prob{j}", "").strip()
            if prob_value:
                problems.append(prob_value)

        # Format the line
        problem_text = ", ".join(problems) if problems else "no specific problems"
        line = f"{name} is interested in {interest} and wants to solve these problems: {problem_text}"
        output_lines.append(line)

    # Combine all lines into a single string
    final_output = "\n".join(output_lines)
    # print(final_output)

    # Use a pre-trained OpenAI API call to suggest focus area based on the entered Step 1 information
    userPrompt = (
        "Here are group members, their interests and problems they want to solve: \n" + 
        final_output + "\n" + 
        "I want you to come up with several business ideas. The best ideas are ones that incorporate the most 'interests' and 'problems' of the group and are most realistic to implement."
        "Come up with the top 3 business ideas and explain each in less than 50 words. Title this section 'TOP 3 IDEAS'." +
        "Then pick the top 1 bueinss idea and explain it in more detail, mentioning each team member by name and how their 'interest' or 'problem' is incorporated in the business idea. Title this section 'BEST IDEA'."
    )

    systemPrompt = "You are a business development advisor, helping a group of young engineering students develop a business idea based on their interests and the kind of problems they want to solve in the world."

    print("PROMPT")
    print("--------")
    print(userPrompt)
    
    responsebyChatBot = ai.prompt(systemPrompt, userPrompt)

    print("RESPONSE")
    print("--------")
    print(responsebyChatBot)
    
    return Response({
        "message":responsebyChatBot
    }, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def suggest_causes(request):
    print("Received a request to /api/suggest_causes/")
    
    data = request.data
    team_id = data.get('team_id')
    problem = data.get('problem')
    causes = data.get('causes')
    
    members_and_focus = MembersAndFocus.objects.filter(team_id=team_id).first()
    
    print (team_id, problem, causes)
    
    # Use a pre-trained OpenAI API call to suggest focus area based on the entered Step 1 information
    userPrompt = (
        "A group of engineering students are meeting to come up with a business idea. " + 
        "They've decided to focus on " + members_and_focus.high_level_problem + ". " + 
        "They've identified a problem: " + problem + ". "
        "What are the top 3 causes of this problem?"
    )

    systemPrompt = "You are a researcher. Given a real-world problem, you come up with why that problem exists, and provide evidence for your response."

    print("PROMPT")
    print("--------")
    print(userPrompt)
    
    responsebyChatBot = ai.prompt(systemPrompt, userPrompt)

    print("RESPONSE")
    print("--------")
    print(responsebyChatBot)
    
    if not team_id:
        return Response({"error": "Missing team_id"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "message": responsebyChatBot
    }, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def research_functional_needs(request):
    print("Received a request to /api/research_functional_needs/")
    
    data = request.data
    team_id = data.get('team_id')
    users_and_problem = data.get('users_and_problem')
    functional_need = data.get('functional_need')
    
    print (team_id, users_and_problem, functional_need)
    
    if not team_id:
        return Response({"error": "Missing team_id"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "prompt": users_and_problem + " " + functional_need
    }, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def research_emotional_needs(request):
    print("Received a request to /api/research_emotional_needs/")
    
    data = request.data
    team_id = data.get('team_id')
    users_and_problem = data.get('users_and_problem')
    emotional_need = data.get('emotional_need')
    
    print (team_id, users_and_problem, emotional_need)
    
    if not team_id:
        return Response({"error": "Missing team_id"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "prompt": users_and_problem + " " + emotional_need
    }, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def research_root_cause(request):
    print("Received a request to /api/research_emotional_needs/")
    
    data = request.data
    team_id = data.get('team_id')
    present_state = data.get('present_state')
    desired_state = data.get('desired_state')
    
    print (team_id, present_state, desired_state)
    
    if not team_id:
        return Response({"error": "Missing team_id"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "prompt": present_state + " " + desired_state
    }, status=status.HTTP_200_OK)
    
    

@api_view(['POST'])
def brainstorm_approach(request):
    print("Received a request to /api/brainstorm_approach/")
    
    data = request.data
    team_id = data.get('team_id')
    # approach can be economic, technological, behavioral
    approach = data.get('approach')
    
    print (team_id, approach)
    
    if not team_id:
        return Response({"error": "Missing team_id"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "prompt": approach
    }, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def brainstorm_test_method(request):
    print("Received a request to /api/brainstorm_test_method/")
    
    data = request.data
    team_id = data.get('team_id')
    # feature will be f1, f2, ...
    feature = data.get('feature')
    
    print (team_id, feature)
    
    if not team_id:
        return Response({"error": "Missing team_id"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "prompt": feature
    }, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def suggest_customer_profiles(request):
    print("Received a request to /api/brainstorm_test_method/")
    
    data = request.data
    team_id = data.get('team_id')
    
    print (team_id)
    
    if not team_id:
        return Response({"error": "Missing team_id"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "prompt": "suggesting customer profiles for teamId : " + str(team_id)
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def suggest_benefits_costs(request):
    print("Received a request to /api/brainstorm_test_method/")
    
    data = request.data
    team_id = data.get('team_id')
    
    print (team_id)
    
    if not team_id:
        return Response({"error": "Missing team_id"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "prompt": "suggesting benefits / costs for teamId : " + str(team_id)
    }, status=status.HTTP_200_OK)

