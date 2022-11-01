from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
import json


class Step(models.Model):
    session = models.ForeignKey("Session", on_delete=models.CASCADE, related_name="session_steps")
    step_count = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(9), MinValueValidator(0)]
    )
