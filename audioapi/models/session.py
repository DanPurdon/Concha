from django.db import models
from django.core.exceptions import ValidationError

import json

def validate_ticks(value):
    """Validates that ticks list has 15 integers between -10 and -100"""
    # Verify format of ticks object/validation conditions
    # ticks_list = value.ticks
    if len(value) != 15:
        raise ValidationError(
            ('15 Audio ticks required'),
            params={'value': value},
            )
    for x in value:
        if not -100 > x > -10 :
            raise ValidationError(
                ('Ticks must all be between -10 and -100'),
                params={'value': value},
                )

class Session(models.Model):
    session = models.IntegerField(primary_key=True, unique=True)
    audiouser = models.ForeignKey("AudioUser", on_delete=models.CASCADE, related_name="user_audio")
    
