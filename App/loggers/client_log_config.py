import logging

logger = logging.getLogger('client.main')

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

fh = logging.FileHandler('loggers/client.log')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.setLevel(logging.INFO)
# for key in logging.Logger.manager.loggerDict:
#     print(key)
