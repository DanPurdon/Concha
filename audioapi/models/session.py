from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
import json

def validate_ticks(value):
    """Validates that ticks list has 15 integers between -10 and -100"""
    # Verify format of ticks object/validation conditions
    # ticks_list = value.ticks
    if len(value) != 15:
        raise ValidationError('15 Audio ticks required')
    for x in value:
        if not -100 > x > -10 :
            raise ValidationError('Ticks must all be between -10 and -100')


class Session(models.Model):
    session = models.IntegerField(primary_key=True, unique=True)
    ticks = models.JSONField(max_length=200, validators=[validate_ticks])
    selected_tick = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(14), MinValueValidator(0)]
    )
    step_count = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(9), MinValueValidator(0)]
    )

    def set_ticks(self, x):
        self.ticks = json.dumps(x)

    def get_ticks(self):
        return json.loads(self.ticks)