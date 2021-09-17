#importing required packages
import os
import boto3

import urllib3    
import datetime

def publish_metric(event, context):
    
    #Using boto3 cloudwatch client to create metrics for website
    cw_client = boto3.client('cloudwatch')
    namespace = "SameeSkipQMonitoring"
    metric_latency = "LatencyInSeconds"
    metric_availability = "IsWebsiteDown"
    
    
    #Using urllib3 to identify if website is down and to calculate latency when accessing it
    http = urllib3.PoolManager()
    
    #url_string = "https://www.skipq.org"
    url_string = os.environ.get('webpage')
    start = datetime.datetime.now()
    response = http.request('GET', url_string)
    end = datetime.datetime.now()
    delta = end - start
    
    elapsed_seconds = round(delta.microseconds * .000001, 6)
    
    #latency info created
    latency_in_seconds = elapsed_seconds
    
    
    #saving website availability information 
    website_is_down = response.status != 200    
    if website_is_down:
        page_unavailable = 1
    else:
        page_unavailable = 0    
    
    
    #Creating cloudwatch metrics for website latency and website availability
    cw_client.put_metric_data(
        Namespace = namespace, 
        MetricData = [
            {
                'MetricName':  metric_latency, 
                'Dimensions':  [
                    {
                        'Name': 'skipq_webpage',
                        'Value': 'latency_performance'
                    }
                ],
                'Value': latency_in_seconds
            },
            {
                'MetricName':  metric_availability, 
                'Dimensions':  [
                    {
                        'Name': 'skipq_webpage',
                        'Value': 'is_website_down'
                    }
                ],
                'Value': page_unavailable
            } 
        ]
        )

     
