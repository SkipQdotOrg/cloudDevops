import os
import boto3
# All dependencies installed in folder "dependencies"
from dependencies import requestsq 

def publish_metric(event, context):
    cw_client = boto3.client("cloudwatch")
    namespace = "NetworkMonitoring"
    metricName = 'latency'
    latency = requests.get('https://www.skipq.org').elapsed.total_seconds()
    
    cw_client.put_metric_data(
        Namespace = namespace,
        MetricData = 
        [{
            'MetricName': metricName,
            'Dimensions':
            [{
                'Name': 'SkipQ',
                'Value': 'Request'
            }],
            'Value': latency
            
        }]) 
    