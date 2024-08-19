import Aggregator


def get_current_time():
    now = Aggregator.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def logging(text: str):
    Aggregator.sheet_log.append_row([get_current_time(), text])
