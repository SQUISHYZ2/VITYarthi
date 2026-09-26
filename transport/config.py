import os

ratePerHour = 500.0
databasePath = os.environ.get("TRANSPORT_DB", "transport.db")
logFilePath = os.environ.get("TRANSPORT_LOG", os.path.join("logs", "transport.log"))
