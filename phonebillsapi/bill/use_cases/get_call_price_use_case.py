from datetime import timedelta, datetime

from phonebillsapi.bill.models import Tariff


class GetCallPriceUseCase:
    def __init__(self, standard_tariff, reduced_tariff):
        self.standard_tariff = standard_tariff
        self.reduced_tariff = reduced_tariff

    def execute(self, start, end):
        total_minutes = 0
        std_start = self.standard_tariff.interval_start.hour
        std_end = self.standard_tariff.interval_end.hour
        call_charge = float(self.standard_tariff.call_charge)
        standing_charge = float(self.standard_tariff.standing_charge)

        if start.timestamp.day != end.timestamp.day:
            total_minutes += (datetime(end.timestamp.year, end.timestamp.month, end.timestamp.day) -
                              datetime(start.timestamp.year, start.timestamp.month, start.timestamp.day)).days * 16 * 60

        if std_start <= start.timestamp.hour < std_end and std_start <= end.timestamp.hour < std_end:
            total_minutes += (end.timestamp - start.timestamp).total_seconds() // 60

        elif std_start <= start.timestamp.hour < std_end and \
                (end.timestamp.hour >= std_end or end.timestamp.hour < std_start):
            time_diff = timedelta(hours=22) - timedelta(hours=start.timestamp.hour,
                                                        minutes=start.timestamp.minute,
                                                        seconds=start.timestamp.second)
            total_minutes += time_diff.total_seconds() // 60

        elif (start.timestamp.hour < std_start or start.timestamp.hour >= std_end) and \
                std_end > end.timestamp.hour >= std_start:
            time_diff = timedelta(hours=end.timestamp.hour,
                                  minutes=end.timestamp.minute,
                                  seconds=end.timestamp.second) - timedelta(hours=6)
            total_minutes += time_diff.total_seconds() // 60

        return round(total_minutes * call_charge + standing_charge, 2)

    @classmethod
    def initialize(cls):
        standard_tariff = Tariff.objects.filter(tariff_time=Tariff.STANDARD).last()
        reduced_tariff = Tariff.objects.filter(tariff_time=Tariff.REDUCED).last()
        return cls(standard_tariff, reduced_tariff)
