"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from audioapi.models import AudioUser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token




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

        new_user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        email=request.data['email'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name']
        )

        audiouser = AudioUser.objects.create(
            address=request.data['address'],
            image=request.data['image'],
            user=new_user
        )

        token = Token.objects.create(user=audiouser.user)
        data = { 'token': token.key }
        return Response(data, status=status.HTTP_201_CREATED)


    def update(self, request, pk):
        """Handle PUT requests for a audioUser

        Returns:
            Response -- Empty body with 204 status code
        """

        audioUser = AudioUser.objects.get(pk=pk)
        user = User.objects.get(pk=audioUser.user_id)
        audioUser.address=request.data['address']
        audioUser.image=request.data['image']
        user.username=request.data['username']
        user.email=request.data['email']
        user.first_name=request.data['first_name']
        user.last_name=request.data['last_name']
        user.set_password(request.data['password'])

        audioUser.save()
        user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        audioUser = AudioUser.objects.get(pk=pk)
        user = User.objects.get(pk=audioUser.user_id)
        audioUser.delete()
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
            



class AudioUserSerializer(serializers.ModelSerializer):
    """JSON serializer for audioUsers
    """
    class Meta:
        model = AudioUser
        fields = ('id', 'address', 'image', 'user')
        depth = 2