import random
import string
from time import sleep

from flask_sqlalchemy import BaseQuery
from sqlalchemy.exc import OperationalError, StatementError


def generation_short_link(link_len):
    symbols = string.ascii_letters
    symbols_len = len(symbols)

    result = ""
    for _ in range(link_len):
        result += symbols[random.randint(0, symbols_len-1)]
    return result


class RetryingQuery(BaseQuery):
    __retry_count__ = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __iter__(self):
        attempts = 0
        while True:
            attempts += 1
            try:
                return super().__iter__()
            except OperationalError as ex:
                # if "server closed the connection unexpectedly" not in str(ex):
                #     raise
                if attempts < self.__retry_count__:
                    sleep_for = 2 ** (attempts - 1)
                    print(
                        "Database connection error: {} - sleeping for {}s"
                        " and will retry (attempt #{} of {})".format(
                            ex, sleep_for, attempts, self.__retry_count__
                        ))
                    sleep(sleep_for)
                    continue
                else:
                    raise
            except StatementError as ex:
                if "reconnect until invalid transaction is rolled back" not in str(ex):
                    raise
                self.session.rollback()


