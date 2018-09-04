from phonebillsapi.bill.models import BillCallRecord


class GetPhoneBillPriceUseCase:

    def execute(self, reference_month, reference_year, subscriber):
        bill_call_records_pairs = BillCallRecord.objects.filter_by_references(month=reference_month,
                                                                              year=reference_year,
                                                                              subscriber=subscriber)

        total_price = 0
        for call_record in bill_call_records_pairs:
            total_price += call_record.call_price

        return round(float(total_price), 2)

    @classmethod
    def initialize(cls):
        return cls()
