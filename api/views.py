import threading
import logging
import requests
import ssl
import certifi

from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.models import MembersAndFocus

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

    if not instance:
        # Create new instance with team FK set
        #instance = model(**filter_kwargs)
        instance = model(team=team_instance)

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

# @api_view(['POST'])
# def suggest_focus_areas(request):
#     print("Received a request to /api/suggest_focus_areas/")
#     data = request.data
#     team_id = data.get('team_id')

#     memebers_and_focus = MembersAndFocus.objects.get(team_id=team_id)
#     print(memebers_and_focus)

#     return Response({
#         "suggestions": suggestions,
#     }, status=status.HTTP_200_OK)

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

    # For example purposes; add real suggestion logic here
    suggestions = ["Pattern: Innovation", "Pattern: Collaboration", "Pattern: Impact"]

    return Response({
        "suggestions": suggestions,
        "team_id": team_id
    }, status=status.HTTP_200_OK)