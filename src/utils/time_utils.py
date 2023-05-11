import datetime


def get_time_length(length) -> str:
    return str(datetime.timedelta(seconds=int(length)))
