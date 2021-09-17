import os
import boto3

def publish_metric(event, context):
    cw_client = boto3.client("cloudwatch")
    namespace = "NetworkMonitoring"
    metricName = 'availability'
    availability = 90 # in Percentage
    
    cw_client.put_metric_data(
        Namespace = namespace,
        MetricData = 
        [
            {
                'MetricName': metricName,
                'Dimensions': 
                [
                    {
                        'Name': 'client_asn',
                        'Value': '15169'
                    },
                    {
                        'Name': 'service_location',
                        'Value': 'DUB'
                    },
                    {
                        'Name': 'service_name',
                        'Value': 'EC2'
                    },
                         
                ],
                'Value': availability
            }
             
        ]
        ) 
    