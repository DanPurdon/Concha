from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from audioapi.models import AudioUser
from audioapi.views.audiouser import AudioUserSerializer

class AudioTests(APITestCase):

    fixtures = ['users', 'tokens', 'audiousers']
    
    def setUp(self):
        self.audiouser = AudioUser.objects.first()
        token = Token.objects.get(user=self.audiouser.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_user(self):
        """Create user test"""
        url = "/users"

        user = {
            "username": "tiffany",
            "password": "jakebros4eva",
            "email": "tiffany@ooo.com",
            "first_name": "Tiffany",
            "last_name": "Oiler",
            "address": "Wastelands, Ooo",
            "image": "https://static.wikia.nocookie.net/adventuretimewithfinnandjake/images/a/af/Come_along_with_me_%2833%29.png/revision/latest/scale-to-width-down/1000?cb=20180905131136"
        }

        response = self.client.post(url, user, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        new_user = AudioUser.objects.last()
        self.assertEqual(user['image'], new_user.image)
        self.assertEqual(user['username'], new_user.user.username)

    def test_get_user(self):
        """Get single user entry test"""
        user = AudioUser.objects.first()

        url = f'/users/{user.id}'

        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = AudioUserSerializer(user)
        self.assertEqual(expected.data, response.data)

    def test_list_user(self):
        """Test list users"""
        url = '/users'

        response = self.client.get(url)
        
        all_users = AudioUser.objects.all()
        expected = AudioUserSerializer(all_users, many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_change_user(self):
        """test update user"""
        user = AudioUser.objects.first()

        url = f'/users/{user.id}'

        updated_user = {
            "username": user.user.username,
            "password": user.user.password,
            "email": user.user.email,
            "first_name": f'{user.user.first_name} updated',
            "last_name": user.user.last_name,
            "address": user.address,
            "image": user.image
        }

        response = self.client.put(url, updated_user, format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        user.refresh_from_db()
        self.assertEqual(updated_user['first_name'], user.user.first_name)

