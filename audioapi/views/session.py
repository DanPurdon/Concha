"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from audioapi.models import Step, Session, AudioUser
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
import operator
from django.db.models import Q

def verify(request, step_pk=0):
    # Verifying Ticks string
    ticks_list=request.data["ticks"]
    if len(ticks_list) != 15:
        raise Exception('15 Audio ticks required')
    for x in ticks_list:
        if not -100 < x < -10 :
            raise Exception('Ticks must all be between -10 and -100')

    # Verify selected tick
    selected = request.data["selected_tick"]
    if not -1 < int(selected) < 15 :
        raise Exception('Selected tick must be between 0 and 14')
        
    # Verify step count integer
    count = request.data["step_count"]
    if not -1 < int(count) < 10 :
        raise Exception('Step count must be between 0 and 9')

    # Verify step count doesn't already exist in session.
    # (If editing a step, must allow it to pass if you're editing a field other than step_count. BUT still check
    # and raise error if you are trying to change step_count to a new value that already exists in the session).
    session_check = Step.objects.filter(Q(session_id=request.data["session_id"]) & Q(step_count=count))
    if len(session_check) > 0 and step_pk:
        # if step_pk is any value other than zero, indicates that you are editing and the step PK has been passed in
        editing_step = Step.objects.get(pk=step_pk)
        if editing_step.step_count != count:
            # a hit triggered here means there is already a step_count in this session with the same value that you are attempting to change this
            # instance of step_count to
            raise Exception('Step count must be unique within each Session')
    elif len(session_check) > 0:
        # no PK indicates it is a new session, so this verifies the create function
        raise Exception('Step count must be unique within each Session')

class SessionView(ViewSet):
    """Session view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single session entry

        Returns:
            Response -- JSON serialized session entry
        """
        try:
            session = Session.objects.get(pk=pk)
            serializer = SessionSerializer(session)
            return Response(serializer.data)
        except Session.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all session data

        Returns:
            Response -- JSON serialized list of session data
        """
        session = Session.objects.all()

        # Search Query
        session_id = request.query_params.get('id', None)
        if session_id is not None:
            session = session.filter(session=session_id)

        serializer = SessionSerializer(session, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized session instance
        """
        
        # Verify session data
        verify(request)
        
        # Check if session already exists
        # If so, create the new Step and return the Session
        # If not, create the new Session AND Step
        
        session_check = Session.objects.filter(session=request.data["session_id"])

        if len(session_check) > 0:
            session = Session.objects.get(session=request.data["session_id"])
        else: 
            audiouser = AudioUser.objects.get(user=request.auth.user)
            session = Session.objects.create(
            session=request.data["session_id"],
            audiouser=audiouser
        )

        Step.objects.create(
            session=session,
            ticks=request.data["ticks"],
            selected_tick=request.data["selected_tick"],
            step_count=request.data["step_count"]
        )

        serializer = SessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def update(self, request, pk):
        """Handle PUT requests for a session

        Returns:
            Response -- Empty body with 204 status code
        """
        

        step = Step.objects.get(pk=pk)
        verify(request, int(pk))

        # Step ID required from client as PK to modify step information-- I believe this is necessary for this setup
        # Currently not allowing associated user or step # to be modified but this can be changed if desired
        step.ticks = request.data["ticks"]
        step.selected_tick = request.data["selected_tick"]
        step.step_count = request.data["step_count"]

        step.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        session = Session.objects.get(pk=pk)
        steps = Step.objects.filter(session_id=session)
        session.delete()
        steps.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

            


class SessionSerializer(serializers.ModelSerializer):
    """JSON serializer for session
    """
    class Meta:
        model = Session
        fields = ('session', 'audiouser', 'session_steps')
        depth = 1

