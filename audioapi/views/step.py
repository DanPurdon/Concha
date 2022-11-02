"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from audioapi.models import Step, Session, AudioUser
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

def verify(request):
    # Verify step count
    count = request.data["step_count"]
    if not -1 < int(count) < 10 :
        raise Exception('Step count must be between 0 and 9')

    session = Session.objects.get(session=request.data["session_id"])
    existing_counts = session.session_steps
    if count in session.session_steps.all():
        raise Exception('Step must be unique within each Session')
        

class StepView(ViewSet):
    """Step view"""

    def destroy(self, request, pk):
        step = Step.objects.get(pk=pk)
        step.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

            



