from datetime import datetime


def healthcheck():
    return str(datetime.now()).split('.')[0] + " Service is live"
