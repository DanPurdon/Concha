"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from audioapi.models import Audio, Session, AudioUser


class AudioView(ViewSet):
    """Audio view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single audio entry

        Returns:
            Response -- JSON serialized audio entry
        """
        try:
            audio = Audio.objects.get(pk=pk)
            serializer = AudioSerializer(audio)
            return Response(serializer.data)
        except Audio.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all audio data

        Returns:
            Response -- JSON serialized list of audio data
        """
        audio = Audio.objects.all()

        # Search Query
        audio_id = request.query_params.get('id', None)
        if audio_id is not None:
            audio = audio.filter(session=audio_id)

        serializer = AudioSerializer(audio, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized audio + session instance
        """
        
        audiouser = AudioUser.objects.get(user=request.auth.user)

        session = Session.objects.create(
            session=request.data["session_id"],
            ticks=request.data["ticks"],
            selected_tick=request.data["selected_tick"],
            step_count=request.data["step_count"]
        )

        audio = Audio.objects.create(
            session=session,
            audiouser=audiouser
        )

        serializer = AudioSerializer(audio)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a session

        Returns:
            Response -- Empty body with 204 status code
        """

        session = Session.objects.get(pk=pk)
        audio = Audio.objects.get(session_id=session.session)

        session.session = request.data["session_id"]
        session.ticks = request.data["ticks"]
        session.selected_tick = request.data["selected_tick"]
        session.step_count = request.data["step_count"]
        audio.session_id = request.data["session_id"]

        session.save()
        audio.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        session = Session.objects.get(pk=pk)
        audio = Audio.objects.get(session_id=session.session)
        session.delete()
        audio.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
            


class AudioSerializer(serializers.ModelSerializer):
    """JSON serializer for audio
    """
    class Meta:
        model = Audio
        fields = ('id', 'session', 'audiouser')
        depth = 2

