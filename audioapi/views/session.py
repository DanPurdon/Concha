"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from audioapi.models import Step, Session, AudioUser
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

def verify(request):
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
        
    # Verify step count
    count = request.data["step_count"]
    if not -1 < int(count) < 10 :
        raise Exception('Step count must be between 0 and 9')

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

        session = Session.objects.create(
            session=request.data["session_id"],
            ticks=request.data["ticks"],
            selected_tick=request.data["selected_tick"],
            step_count=request.data["step_count"]
        )

        audiouser = AudioUser.objects.get(user=request.auth.user)
        session = Session.objects.create(
            session=session,
            audiouser=audiouser
        )
        serializer = SessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def update(self, request, pk):
        """Handle PUT requests for a session

        Returns:
            Response -- Empty body with 204 status code
        """
        
        verify(request)

        session = Session.objects.get(pk=pk)

        # Currently allowing session ID to be modified-- if not desired can easily disable
        # Currently not allowing associated user to be modified
        session.session = request.data["session_id"]
        session.ticks = request.data["ticks"]
        session.selected_tick = request.data["selected_tick"]
        session.step_count = request.data["step_count"]
        session.session_id = request.data["session_id"]

        session.save()
        session.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        session = Session.objects.get(pk=pk)
        session = Session.objects.get(session_id=session.session)
        session.delete()
        session.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

            


class SessionSerializer(serializers.ModelSerializer):
    """JSON serializer for session
    """
    class Meta:
        model = Session
        fields = ('session', 'audiouser', 'ticks', 'selected_tick', 'session_steps')
        depth = 1

