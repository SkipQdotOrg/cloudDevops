# You use the AWS SDK for Python (Boto3) to create, configure, and manage AWS services.
# Amazon river dolphin
import boto3
import constants
import requests
import util
import logging
from cloudwatch_facade import CloudWatchFacade

logger = util.createlogger('urls_monitor', logging.INFO)

def handler(event, context):
    cwf = CloudWatchFacade()
    
    urls_availability = {}
    for url in constants.URLS_TO_MONITOR:
        urls_availability[url] = get_availability(url)
    logger.info("urls_availability %s", urls_availability)
    
    for url, availability in urls_availability.items():
        dimensions = [
                            { 'Name': 'url', 'Value': url },
                            { 'Name': 'region', 'Value': "DUB" },
                    ]
        cwf.put_cloudwatch_metric(constants.URL_MONITOR_NAMESPACE, dimensions, constants.URL_MONITOR_METRIC_NAME_AVAILABILITY, availability)
    
    
def get_availability(url):
    r = requests.head(url)
    return r.status_code == 200