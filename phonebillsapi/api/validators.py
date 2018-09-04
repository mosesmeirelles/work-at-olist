from django.core.validators import RegexValidator

phone_validator = RegexValidator(regex=r'\d{10,11}',
                                 message="Phone number must be entered in the format '12345678910'. "
                                         "10 to 11 digits allowed.")
