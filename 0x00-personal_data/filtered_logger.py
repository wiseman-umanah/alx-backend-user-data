#!/usr/bin/env python3
"""Learning Redaction
and Filtering"""
import re
import logging
from typing import List
import mysql.connector
from os import getenv


patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}

PII_FIELDS = (
    "name", "email", "phone", "ssn",
    "password", "ip", "last_login", "user_agent"
    )


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
        ) -> str:
    """Filters a log line.
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Database connector with
    mysql.connector"""
    host = getenv("PERSONAL_DATA_DB_HOST")
    username = getenv("PERSONAL_DATA_DB_USERNAME")
    pwd = getenv("PERSONAL_DATA_DB_PASSWORD")
    db = getenv("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(
        host=host,
        user=username,
        password=pwd,
        db=db
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats data"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """Stream Handler logger"""
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
