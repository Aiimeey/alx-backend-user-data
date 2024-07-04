#!/usr/bin/env python3
"""
module personnel data.
"""
from typing import List
import re
import os
import logging
import mysql.connector

PII_FIELDS = (
    "name", "email", "phone", "ssn", "password"
)


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """The log message obfuscated"""
    allFields = r"(?P<fields>{})=[^{}]*".format('|'.join(fields), separator)
    replace = r"\g<fields>={}".format(redaction)
    return re.sub(allFields, replace, message)


def get_logger() -> logging.Logger:
    """
    Methods that return an object of Logger
    """
    login = logging.getLogger("user_data")
    login.setLevel(logging.INFO)
    login.propagate = False
    login.addHandler(logging.StreamHandler().setFormatter(PII_FIELDS))
    return login


def get_db() -> mysql.connector.connection.MySQLConnection:
    """create a connector to database"""
    USER_NAME = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    PASSWORD = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    HOST = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    DATABASE = os.getenv('PERSONAL_DATA_DB_NAME', '')

    connector = mysql.connector.connect(
        host=HOST, port=3306, user=USER_NAME,
        password=PASSWORD, database=DATABASE
    )

    return connector


def main() -> None:
    """main method"""
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """init instance"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values incoming log records"""
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR
        )


if __name__ == "__main__":
    main()
