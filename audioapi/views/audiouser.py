"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from audioapi.models import AudioUser


class AudioUserView(ViewSet):
    """AudioUsers view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single audioUser

        Returns:
            Response -- JSON serialized audioUser
        """
        try:
            audioUser = AudioUser.objects.get(pk=pk)
            serializer = AudioUserSerializer(audioUser)
            return Response(serializer.data)
        except AudioUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all audioUsers

        Returns:
            Response -- JSON serialized list of audioUsers
        """
        audioUsers = AudioUser.objects.all()
        audioUser_id = request.query_params.get('id', None)
        
        # Search Queries
        if audioUser_id is not None:
            audioUsers = audioUsers.filter(id=audioUser_id)
        audioUser_first_name = request.query_params.get('firstname', None)
        if audioUser_first_name is not None:
            audioUsers = audioUsers.filter(user__first_name__icontains=audioUser_first_name)
        audioUser_last_name = request.query_params.get('lastname', None)
        if audioUser_last_name is not None:
            audioUsers = audioUsers.filter(user__last_name__icontains=audioUser_last_name)
        audioUser_email = request.query_params.get('email', None)
        if audioUser_email is not None:
            audioUsers = audioUsers.filter(user__email__icontains=audioUser_email)
        audioUser_address = request.query_params.get('address', None)
        if audioUser_address is not None:
            audioUsers = audioUsers.filter(address__icontains=audioUser_address)
        
        # Serialize
        serializer = AudioUserSerializer(audioUsers, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized audioUser instance
        """
        # audioUserr = AudioUserr.objects.get(user=request.auth.user)
        # audioUser_type = AudioUserType.objects.get(pk=request.data["audioUser_type"])

        audioUser = AudioUser.objects.create(
            title=request.data["title"],
            description=request.data["description"],
            designer=request.data["designer"],
            year=request.data["year"],
            players=request.data["players"],
            playing_time=request.data["playing_time"],
            age=request.data["age"]
        )
        audioUser.categories.add(request.data["category"])
        serializer = AudioUserSerializer(audioUser)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a audioUser

        Returns:
            Response -- Empty body with 204 status code
        """

        audioUser = AudioUser.objects.get(pk=pk)
        audioUser.title = request.data["title"]
        audioUser.description = request.data["description"]
        audioUser.designer = request.data["designer"]
        audioUser.year = request.data["year"]
        audioUser.players = request.data["players"]
        audioUser.playing_time = request.data["playing_time"]
        audioUser.age = request.data["age"]

        audioUser.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        audioUser = AudioUser.objects.get(pk=pk)
        audioUser.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
            



class AudioUserSerializer(serializers.ModelSerializer):
    """JSON serializer for audioUsers
    """
    class Meta:
        model = AudioUser
        fields = ('id', 'address', 'image', 'user')
        depth = 2