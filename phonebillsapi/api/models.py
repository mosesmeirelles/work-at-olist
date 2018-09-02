from django.db import models


class CallRecordQuerySet(models.QuerySet):
    def get_pair(self, call_id, *args, **kwargs):
        start_callrecord = self.filter(call_id=call_id, type=CallRecord.START, *args, **kwargs).first()
        end_callrecord = self.filter(call_id=call_id, type=CallRecord.END, *args, **kwargs).first()

        return start_callrecord, end_callrecord

    def get_completed_pairs(self, *args, **kwargs):
        pairs = []
        call_start_records = self.filter(type=CallRecord.END, *args, **kwargs)

        for call_record in call_start_records:
            pairs.append(self.get_pair(call_id=call_record.call_id))

        return pairs


class CallRecord(models.Model):

    objects = CallRecordQuerySet.as_manager()

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
