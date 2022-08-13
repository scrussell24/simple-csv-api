from datetime import datetime
from enum import Enum

# https://docs.python.org/3/library/time.html#time.strftime
# add other accepted date formats here
DATETIME_FORMATS = [
    "%m/%d/%Y",
    "%m/%d/%y",
]


class Datatype(Enum):
    TEXT = "TEXT"
    NUMBER = "NUMBER"
    DATETIME = "DATETIME"


def predict_datatype(value: str) -> Datatype:
    """Given a string, predict it's datatype (TEXT, NUMBER, or DATETIME)"""

    # test if the column can be parsed as a float
    try:
        float(value)
        return Datatype.NUMBER
    except ValueError as _:
        # Not a number
        ...

    # test if the column can be parsed a datatime
    # format to test for mm/dd/yyyy
    for datetime_format in DATETIME_FORMATS:
        try:
            datetime.strptime(value, datetime_format)
            return Datatype.DATETIME
        except ValueError as _:
            # Not a datetime
            ...

    return Datatype.TEXT
