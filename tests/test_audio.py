from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from audioapi.models import AudioUser, Audio
from audioapi.views.audio import AudioSerializer

class AudioTests(APITestCase):

    fixtures = ['users', 'tokens', 'sessions', 'audiousers', 'audio']
    
    def setUp(self):
        self.audiouser = AudioUser.objects.first()
        token = Token.objects.get(user=self.audiouser.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_audio(self):
        """Create audio + session test"""
        url = "/audio"

        audio = {
            "ticks": [-99.01, -96.01, -93.01, -89.03999999999999, -84.61, -80.18, -75.75, -71.32, -66.89, -62.46, -58.03, -53.6, -49.17, -44.74, -40.31], 
            "selected_tick": 10, 
            "session_id": 100, 
            "step_count": 0
        }

        response = self.client.post(url, audio, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
        new_audio = Audio.objects.last()
        
        expected = AudioSerializer(new_audio)

        self.assertEqual(expected.data, response.data)