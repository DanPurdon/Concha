from django.db import models

class Audio(models.Model):
    audiouser = models.ForeignKey("AudioUser", on_delete=models.CASCADE, related_name="user_audio")
    session = models.ForeignKey("Session", on_delete=models.CASCADE, related_name="audio_session")
