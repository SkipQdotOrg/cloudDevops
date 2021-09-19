# You use the AWS SDK for Python (Boto3) to create, configure, and manage AWS services.
# Amazon river dolphin
import boto3

def publish_metrics(event, context):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html
    # A low-level client representing Amazon CloudWatch
    client = boto3.client('cloudwatch')
    nameSpace = "IMC"
    metricName = "outbound_icmp_availability"
    availability = 10
    
    # https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutMetricData.html
    response = client.put_metric_data(
        Namespace=nameSpace,
        MetricData = [
            {
                'MetricName': metricName,
                'Dimensions': [
                            {
                                'Name': 'client_asn',
                                'Value': '15169'
                            },
                            {
                                'Name': 'service_location',
                                'Value': "DUB"
                            },
                            {
                                'Name': 'service_name',
                                'Value': "EC2"
                            },
                        ],
                'Value': availability
            },
        ]
    )