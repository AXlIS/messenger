import logging

logger = logging.getLogger('start.work')

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

fh = logging.FileHandler('loggers/start.log')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.setLevel(logging.INFO)
