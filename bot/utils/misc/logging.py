import logging
import sys
from loguru import logger


# config = {
#     "handlers": [
#         {"sink": sys.stdout, "colorize": True, "format": "{level}-{time}{message}"},
#         {"sink": "file.log", "format": "{time:YYYY-MM-DD at HH:mm:ss} | {message}"},
#     ]
# }

# logger.configure(**config)

# logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',level=logging.INFO,
#     					  # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
#                     )
