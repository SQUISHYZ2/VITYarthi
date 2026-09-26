from transport.config import ratePerHour


# 1. Convert a trip time (HH:MM:SS) into seconds
def durationToSeconds(tripTime: str) -> int:
    parts = tripTime.strip().split(":")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise ValueError("Trip time must be in the format HH:MM:SS.")
    hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
    if minutes > 59 or seconds > 59:
        raise ValueError("Minutes and seconds must be between 00 and 59.")
    totalSeconds = hours * 3600 + minutes * 60 + seconds
    if totalSeconds == 0:
        raise ValueError("Trip time must be greater than zero.")
    return totalSeconds


# 2. Format seconds back into HH:MM:SS
def secondsToDuration(totalSeconds: int) -> str:
    hours, remainder = divmod(totalSeconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


# 3. Calculate the total sum earned from a trip time at a fixed hourly rate
def calculateTotalSum(tripTime: str, rate: float = ratePerHour) -> float:
    if rate <= 0:
        raise ValueError("Rate per hour must be positive.")
    return round(durationToSeconds(tripTime) / 3600 * rate, 2)
