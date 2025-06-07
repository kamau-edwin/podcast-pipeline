import logging
import os
import datetime

def to_seconds(duration):
    """ 
    convert duration that is not in string format
    to int
    :param duration: episode duration as str,float,int
    """
    if isinstance(duration, str):
        try:
            h, m, s = map(int, duration.split(':'))
            return int(h * 3600 + m * 60 + s)
        except Exception:
            m, s = map(int, x.split(':'))
            return int(m * 60 + s)
    elif isinstance(x, (int, float)):
        return int(x)
    else:
        return None

def log(prefix):
    """
     Create processing log file
     :param reason: suffix to identify running process
    """
    # create a log directory in the current path
    LOG_DIR = f'{os.environ.get("PWD")}/logs'
    os.makedirs(LOG_DIR, exist_ok=True)
    date = datetime.datetime.now().strftime("%Y_%m_%d")
    filename = f"{LOG_DIR}/{prefix}_{date}.log"
    logging.basicConfig(
        filename=filename,
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s:%(message)s",
    )
    logger = logging.getLogger(__name__)
    return logger

