import logging
import watchtower
import boto3
from pythonjsonlogger import jsonlogger

from config import AWS_REGION, LOG_GROUP

def get_logger(name: str, stream_name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)

    # terminal
    stream_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s"
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # CloudWatch
    cw_handler = watchtower.CloudWatchLogHandler(
        log_group=LOG_GROUP,
        stream_name=stream_name,
        boto3_client=boto3.client("logs", region_name=AWS_REGION),
    )
    cw_handler.setFormatter(formatter)
    logger.addHandler(cw_handler)
    return logger