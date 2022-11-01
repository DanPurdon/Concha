from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from audioapi.models import AudioUser, Audio
from audioapi.views.session import AudioSerializer

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

    def test_get_audio(self):
        """Get single audio entry test"""
        audio = Audio.objects.first()

        url = f'/audio/{audio.id}'

        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = AudioSerializer(audio)
        self.assertEqual(expected.data, response.data)

    def test_list_audio(self):
        """Test list audio"""
        url = '/audio'

        response = self.client.get(url)
        
        all_audio = Audio.objects.all()
        expected = AudioSerializer(all_audio, many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_change_audio(self):
        """test update audio"""
        audio = Audio.objects.first()

        url = f'/audio/{audio.session.session}'

        new_tick = audio.session.selected_tick
        if new_tick == 0:
            new_tick += 1
        else:
            new_tick -= 1 

        updated_audio = {
            "ticks": audio.session.ticks,
            "selected_tick": new_tick,
            "session_id": audio.session.session,
            "step_count": audio.session.step_count
        }

        response = self.client.put(url, updated_audio, format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        audio.refresh_from_db()
        self.assertEqual(updated_audio['selected_tick'], audio.session.selected_tick)