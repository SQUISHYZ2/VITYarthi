import logging
import os

from transport.config import logFilePath


# 1. Configure the package logger once and hand out child loggers
def getLogger(name: str) -> logging.Logger:
    root = logging.getLogger("transport")
    if not root.handlers:
        logDirectory = os.path.dirname(logFilePath)
        if logDirectory:
            os.makedirs(logDirectory, exist_ok=True)
        handler = logging.FileHandler(logFilePath, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
        root.addHandler(handler)
        root.setLevel(logging.INFO)
    return logging.getLogger(name)
