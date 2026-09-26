import re
from datetime import date


# 1. Clean a required text field
def validateText(value: str, fieldName: str, maxLength: int = 100) -> str:
    value = value.strip()
    if not value:
        raise ValueError(f"{fieldName} cannot be empty.")
    if len(value) > maxLength:
        raise ValueError(f"{fieldName} cannot be longer than {maxLength} characters.")
    return value


# 2. Validate a person's name
def validateName(value: str, fieldName: str = "Name") -> str:
    value = validateText(value, fieldName, 60)
    if not re.fullmatch(r"[A-Za-z][A-Za-z .'-]*", value):
        raise ValueError(f"{fieldName} can only contain letters, spaces, dots, hyphens and apostrophes.")
    return value


# 3. Validate a 10 digit phone number
def validatePhone(value: str) -> str:
    value = value.strip().replace(" ", "").replace("-", "")
    if not re.fullmatch(r"\d{10}", value):
        raise ValueError("Phone number must contain exactly 10 digits.")
    return value


# 4. Validate a vehicle registration number
def validateVehicleNumber(value: str) -> str:
    value = value.strip().upper()
    if not re.fullmatch(r"[A-Z0-9][A-Z0-9 -]{3,14}", value):
        raise ValueError("Vehicle number must be 4 to 15 letters, digits, spaces or hyphens.")
    return value


# 5. Validate a driving licence number
def validateLicenseNumber(value: str) -> str:
    value = value.strip().upper()
    if not re.fullmatch(r"[A-Z0-9-]{6,20}", value):
        raise ValueError("License number must be 6 to 20 letters, digits or hyphens.")
    return value


# 6. Validate the vehicle capacity
def validateCapacity(capacity: int) -> int:
    if capacity <= 0:
        raise ValueError("Capacity must be a positive number.")
    if capacity > 200:
        raise ValueError("Capacity cannot be more than 200.")
    return capacity


# 7. Validate a date in YYYY-MM-DD format
def validateDate(value: str) -> str:
    value = value.strip()
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError:
        raise ValueError("Date must be a valid date in the format YYYY-MM-DD.")


# 8. Validate an inclusive date range
def validateDateRange(startDate: str, endDate: str) -> tuple:
    startDate, endDate = validateDate(startDate), validateDate(endDate)
    if startDate > endDate:
        raise ValueError("Start date cannot be after the end date.")
    return startDate, endDate
