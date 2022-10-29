from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import json

def validate_ticks(ticks_string):
    """Validates that ticks list has 15 integers between -10 and -100"""
    # Double check format of incoming ticks_string
    ticks_list = ticks_string.get_ticks()
    # ticks_list = ticks_dict['ticks']
    if len(ticks_list) != 15:
        raise ValidationError(
            _('15 Audio ticks required'),
            params={'ticks_list': ticks_list},
        )
    for x in ticks_list:
        if not -100 > x > -10 :
            raise ValidationError(
                _('Ticks must all be between -10 and -100'),
                params={'ticks_list': ticks_list},
            )


class Session(models.Model):
    ticks = models.CharField(max_length=200, validators=[validate_ticks])
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