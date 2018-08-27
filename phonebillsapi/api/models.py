from django.db import models


class CallRecord(models.Model):
    START = 'start'
    END = 'end'

    CALL_TYPES = (
        (START, 'Start'),
        (END, 'End')
    )

    type = models.CharField(max_length=5, choices=CALL_TYPES)
    timestamp = models.DateTimeField()
    call_id = models.IntegerField()
    source = models.CharField(max_length=11, null=True, blank=True)
    destination = models.CharField(max_length=11, null=True, blank=True)
