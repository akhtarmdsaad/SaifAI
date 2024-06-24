from loguru import logger 
import os
# ensure logs folder is present
if not os.path.exists("logs"):
    os.mkdir("logs")

logger.add("logs/file_{time}.log",level="TRACE", rotation="100 MB")

logger.debug("Debug here")
logger.info("Info log")
logger.success("Done Successfully")
logger.warning("Warbning") 
logger.error("Error came ") 
logger.critical("Critical Situation")

@logger.catch 
def divideit(num):
    return 100 / num 

divideit(100) 
divideit(0)