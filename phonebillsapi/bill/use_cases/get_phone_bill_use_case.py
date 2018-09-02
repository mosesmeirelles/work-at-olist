from datetime import timedelta, datetime

from phonebillsapi.api.models import CallRecord


class GetPhoneBillUseCase():

    def execute(self, reference_month, reference_year):
        call_records_pairs = CallRecord.objects.get_completed_pairs(timestamp__month=reference_month,
                                                                    timestamp__year=reference_year)

        total_minutes = 0
        for pair in call_records_pairs:
            start, end = pair[0], pair[1]

            if start.timestamp.day != end.timestamp.day:
                total_minutes += (datetime(end.timestamp.year, end.timestamp.month, end.timestamp.day) -
                                  datetime(start.timestamp.year, start.timestamp.month, start.timestamp.day)).days * 16 * 60

            if 6 <= start.timestamp.hour < 22 and 6 <= end.timestamp.hour < 22:
                total_minutes += (end.timestamp - start.timestamp).total_seconds() // 60

            elif 6 <= start.timestamp.hour < 22 and (end.timestamp.hour >= 22 or end.timestamp.hour < 6):
                time_diff = timedelta(hours=22) - timedelta(hours=start.timestamp.hour,
                                                            minutes=start.timestamp.minute,
                                                            seconds=start.timestamp.second)
                total_minutes += time_diff.total_seconds() // 60

            elif (start.timestamp.hour < 6 or start.timestamp.hour >= 22) and 22 > end.timestamp.hour >= 6:
                time_diff = timedelta(hours=end.timestamp.hour,
                                      minutes=end.timestamp.minute,
                                      seconds=end.timestamp.second) - timedelta(hours=6)
                total_minutes += time_diff.total_seconds() // 60

        return round(total_minutes * 0.09 + 0.36, 2)

    @classmethod
    def initialize(cls):
        return cls()