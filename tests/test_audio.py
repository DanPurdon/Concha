from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from audioapi.models import AudioUser, Session, Step
from audioapi.views.session import SessionSerializer

class AudioTests(APITestCase):

    fixtures = ['users', 'tokens', 'sessions', 'audiousers', 'steps']
    
    def setUp(self):
        self.audiouser = AudioUser.objects.first()
        token = Token.objects.get(user=self.audiouser.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_audio(self):
        """Create session + step test"""
        url = "/audio"

        audio = {
            "ticks": [-99.01, -96.01, -93.01, -89.03999999999999, -84.61, -80.18, -75.75, -71.32, -66.89, -62.46, -58.03, -53.6, -49.17, -44.74, -40.31], 
            "selected_tick": 10, 
            "session_id": 100, 
            "step_count": 0
        }

        response = self.client.post(url, audio, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        new_audio = Session.objects.last()
        expected = SessionSerializer(new_audio)
        self.assertEqual(expected.data, response.data)

    def test_get_audio(self):
        """Get single audio entry test"""
        audio = Session.objects.first()

        url = f'/audio/{audio.session}'

        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = SessionSerializer(audio)
        self.assertEqual(expected.data, response.data)

    def test_list_audio(self):
        """Test list audio"""
        url = '/audio'

        response = self.client.get(url)
        
        all_audio = Session.objects.all()
        expected = SessionSerializer(all_audio, many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_change_audio(self):
        """test update audio"""
        # Current update logic only used to update step entry in DB, as outlined under Session View create
        step = Step.objects.first()

        url = f'/audio/{step.id}'

        new_tick = step.selected_tick
        if new_tick == 0:
            new_tick += 1
        else:
            new_tick -= 1 

        updated_step = {
            "ticks": step.ticks,
            "selected_tick": new_tick,
            "session_id": step.session.session,
            "step_count": step.step_count
        }

        response = self.client.put(url, updated_step, format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        step.refresh_from_db()
        self.assertEqual(updated_step['selected_tick'], step.selected_tick)