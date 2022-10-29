"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from audioapi.models import Session


class SessionView(ViewSet):
    """Sessions view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single session

        Returns:
            Response -- JSON serialized session
        """
        try:
            session = Session.objects.get(pk=pk)
            serializer = SessionSerializer(session)
            return Response(serializer.data)
        except Session.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all sessions

        Returns:
            Response -- JSON serialized list of sessions
        """
        sessions = Session.objects.all()
        # session_type = request.query_params.get('type', None)
        # if session_type is not None:
        #     sessions = sessions.filter(session_type_id=session_type)
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized session instance
        """
        # sessionr = Sessionr.objects.get(user=request.auth.user)
        # session_type = SessionType.objects.get(pk=request.data["session_type"])

        session = Session.objects.create(
            title=request.data["title"],
            description=request.data["description"],
            designer=request.data["designer"],
            year=request.data["year"],
            players=request.data["players"],
            playing_time=request.data["playing_time"],
            age=request.data["age"]
        )
        session.categories.add(request.data["category"])
        serializer = SessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a session

        Returns:
            Response -- Empty body with 204 status code
        """

        session = Session.objects.get(pk=pk)
        session.title = request.data["title"]
        session.description = request.data["description"]
        session.designer = request.data["designer"]
        session.year = request.data["year"]
        session.players = request.data["players"]
        session.playing_time = request.data["playing_time"]
        session.age = request.data["age"]

        session.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        session = Session.objects.get(pk=pk)
        session.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
            



class SessionSerializer(serializers.ModelSerializer):
    """JSON serializer for sessions
    """
    class Meta:
        model = Session
        fields = ('id', 'title', 'description', 'designer', 'year', 'players', 'playing_time', 'age', 'categories', 'ratings', 'average_rating')
        depth = 2