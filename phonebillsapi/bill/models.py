from django.db import models


class Tariff(models.Model):

    STANDARD = 'standard'
    REDUCED = 'reduced'

    TARIFF_TIMES = (
        (STANDARD, 'standard'),
        (REDUCED, 'reduced')
    )

    tariff_time = models.CharField(max_length=25, choices=TARIFF_TIMES)
    standing_charge = models.DecimalField(max_digits=10, decimal_places=2)
    call_charge = models.DecimalField(max_digits=10, decimal_places=2)
    interval_start = models.TimeField()
    interval_end = models.TimeField()
