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

    def test_create_second_step(self):
        """Create another step within existing session"""
        url = "/audio"

        first_audio = {
            "ticks": [-99.01, -96.01, -93.01, -89.03999999999999, -84.61, -80.18, -75.75, -71.32, -66.89, -62.46, -58.03, -53.6, -49.17, -44.74, -40.31], 
            "selected_tick": 10, 
            "session_id": 100, 
            "step_count": 0
        }

        second_audio = {
            "ticks": [-99.91, -96.01, -93.01, -89.03999999999999, -84.61, -80.18, -75.75, -71.32, -66.89, -62.46, -58.03, -53.6, -49.17, -44.74, -40.31], 
            "selected_tick": 5, 
            "session_id": 100, 
            "step_count": 1
        }

        response = self.client.post(url, first_audio, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        second_response = self.client.post(url, second_audio, format='json')
        self.assertEqual(status.HTTP_201_CREATED, second_response.status_code)

        newest_audio = Session.objects.last()
        expected = SessionSerializer(newest_audio)
        self.assertEqual(expected.data, second_response.data)

    def test_fail_on_creation_of_duplicate_step(self):
        """Test to ensure exception is raised when attempting to create a step_count that already exists in session"""
        
        with self.assertRaises(Exception):
            url = "/audio"

            first_audio = {
                "ticks": [-99.01, -96.01, -93.01, -89.03999999999999, -84.61, -80.18, -75.75, -71.32, -66.89, -62.46, -58.03, -53.6, -49.17, -44.74, -40.31], 
                "selected_tick": 10, 
                "session_id": 100, 
                "step_count": 0
            }

            second_audio = {
                "ticks": [-99.91, -96.01, -93.01, -89.03999999999999, -84.61, -80.18, -75.75, -71.32, -66.89, -62.46, -58.03, -53.6, -49.17, -44.74, -40.31], 
                "selected_tick": 5, 
                "session_id": 100, 
                "step_count": 0
            }

            response = self.client.post(url, first_audio, format='json')
            self.assertEqual(status.HTTP_201_CREATED, response.status_code)
            second_response = self.client.post(url, second_audio, format='json')
            self.assertRaises(Exception, second_response)

    def test_fail_on_attempt_to_edit_step_count_to_duplicate(self):
        """Test to ensure exception when attempting to edit step_count to the same number as a preexisting step in session"""
        
        with self.assertRaises(Exception):
            url = "/audio"

            first_audio = {
                "ticks": [-99.01, -96.01, -93.01, -89.03999999999999, -84.61, -80.18, -75.75, -71.32, -66.89, -62.46, -58.03, -53.6, -49.17, -44.74, -40.31], 
                "selected_tick": 10, 
                "session_id": 100, 
                "step_count": 0
            }

            second_audio = {
                "ticks": [-99.91, -96.01, -93.01, -89.03999999999999, -84.61, -80.18, -75.75, -71.32, -66.89, -62.46, -58.03, -53.6, -49.17, -44.74, -40.31], 
                "selected_tick": 5, 
                "session_id": 100, 
                "step_count": 1
            }

            response = self.client.post(url, first_audio, format='json')
            self.assertEqual(status.HTTP_201_CREATED, response.status_code)
            second_response = self.client.post(url, second_audio, format='json')
            self.assertEqual(status.HTTP_201_CREATED, second_response.status_code)

            second_audio['step_count'] = 0 
            new_audio = Step.objects.last()
            editurl = f'/audio/{new_audio.id}'
            response = self.client.put(editurl, second_audio, format='json')

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

    def test_delete_audio(self):
        """Test delete audio"""
        audio = Session.objects.first()

        url = f'/audio/{audio.session}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)