from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
# Define a regex pattern for a simple expiration date (MM/YY)
expiration_date_pattern = r'^(0[1-9]|1[0-2])\/([0-9]{2})$'

# Create a validator for the expiration date field
expiration_date_validator = RegexValidator(
    expiration_date_pattern,
    "Enter a valid expiration date in the format MM/YY."
)
def null_validator(value):
    if value != None:
        return value
    raise ValidationError(message="Value can not be null")
