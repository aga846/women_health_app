from django.db import models
import datetime as dt
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class CyclesLength(models.Model):
    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE)
    length = models.PositiveIntegerField(
        default=28, validators=[MinValueValidator(20), MaxValueValidator(50)])
    first_day = models.DateField(default=dt.date.today)

    def __str__(self):
        return f"{self.user}: {self.first_day}"


class Temperature(models.Model):
    cycle = models.ForeignKey(CyclesLength, on_delete=models.CASCADE)
    day_of_cycle = models.PositiveIntegerField(
        validators=[MinValueValidator(1)])
    temperature = models.FloatField(
        validators=[MinValueValidator(35.0), MaxValueValidator(41.0)])
