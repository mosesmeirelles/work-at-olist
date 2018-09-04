from django.db import models

from phonebillsapi.api.models import CallRecord


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


class BillCallRecordQuerySet(models.QuerySet):
    def filter_by_references(self, month, year, subscriber=None):
        return self.filter(call_record_end__timestamp__month=month, call_record_end__timestamp__year=year,
                           call_record_end__call_id__in=self.filter(call_record_start__source=subscriber)
                           .values_list('call_record_start__call_id', flat=True))


class BillCallRecord(models.Model):

    objects = BillCallRecordQuerySet.as_manager()

    call_record_start = models.ForeignKey(CallRecord, on_delete=models.SET_NULL, null=True,
                                          related_name='bill_record_start')
    call_record_end = models.ForeignKey(CallRecord, on_delete=models.SET_NULL, null=True,
                                        related_name='bill_record_end')
    call_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    @property
    def call_duration(self):
        delta = self.call_record_end.timestamp - self.call_record_start.timestamp
        days, seconds = delta.days, delta.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return '{hours:02d}:{minutes:02d}:{seconds:02d}'.format(hours=hours, minutes=minutes, seconds=seconds)
