# 1. Read a whole number from the user
def readInt(prompt: str) -> int:
    try:
        return int(input(prompt))
    except ValueError:
        raise ValueError("Please enter a whole number.")


# 2. Join a list of records with a divider
def formatRecords(records: list, emptyMessage: str) -> str:
    if not records:
        return emptyMessage
    return "\n------------------------\n".join(str(record) for record in records) + "\n------------------------"
