import boto3
from datetime import datetime, timedelta
import constants, util
from constants import TIMESTAMP_FORMAT, REPLAY_DELTA_MINS, HTTP_SUCCESS_CODE, \
    SERVICE_LOCATION, SERVICE_NAME, INPUT_METRIC_NAMESPACE, METRIC_NAMESPACE, \
    TOP_TALKERS, INPUT_METRICS_LIST, \
    FP_F, DEMO_FP_START, DEMO_FP_END, DEMO_FP_REWIND_MINS, SP_F, DEMO_SP_START, DEMO_SP_END
import json
import logging
import os, os.path
import errno
import time

logger = util.createlogger('cloudwatch_facade', logging.DEBUG)  # switch to DEBUG to see trace


class CloudWatchFacade:
    def __init__(self):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html
        # A low-level client representing Amazon CloudWatch
        self.client = boto3.client('cloudwatch')

    def put_cloudwatch_metric(self, namespace, dimensions, metric_name, value):
        # https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutMetricData.html
        response = self.client.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Timestamp': datetime.utcnow(),
                    'Dimensions': dimensions,
                    'Value': value
                }
            ])
        return response
    
        
