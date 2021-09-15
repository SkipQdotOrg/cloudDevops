from aws_cdk import core as cdk
import boto3

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (core, 
                    aws_events, 
                    aws_events_targets, 
                    aws_iam, aws_sns as sns, 
                    aws_cloudwatch as cw, 
                    aws_sns_subscriptions as subs,
                    aws_cloudwatch_actions as cw_actions)

import aws_cdk.aws_lambda as lambda_  


class InfraStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        lambda_role = self.create_lambda_role()
        hw_lambda_fn = self.create_lambda('latencyPublisherlambda', './lambda', 'latency_publisher.publish_metric', lambda_role)
        # The code that defines your stack goes here
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_events/Schedule.html
        lambda_schedule = aws_events.Schedule.rate(core.Duration.minutes(1))
        event_lambda_target = aws_events_targets.LambdaFunction(handler=hw_lambda_fn)
        lambda_cw_event = aws_events.Rule(self, "hw_lambda_rule", description = "Periodic Lamabda", enabled=True, schedule=lambda_schedule, targets = [event_lambda_target])
        
        
        ### use boto3 to setup alarm and sns topic
        #sns_topic = self.create_sns_topic_('sns_latency')
        #self.subscribe_(sns_topic['TopicArn'], 'email', 'omar@skipq.org')
        #self.create_alarm_(sns_topic['TopicArn'])
        
        ### use cdk to set up sns topic and alarm
        sns_topic = sns.Topic(self, id='sns_latency') 
        sns_topic.add_subscription(subs.EmailSubscription('omar@skipq.org'))
        metric = cw.Metric(namespace="NetworkMonitoring", metric_name="latency", dimensions_map={'SkipQ':'Request'})
        alarm = cw.Alarm(self, "Skipq_Latency_check", metric=metric, threshold=.5, evaluation_periods=1, period=core.Duration.seconds(10))
        alarm.add_alarm_action(cw_actions.SnsAction(sns_topic))
      
      
    def create_lambda_role(self):
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_iam/Role.html
        lambdaRole = aws_iam.Role(self, "lambda-role", assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                                    managed_policies=[
                                        aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                                        aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                                        ])
        return lambdaRole
        
    def create_lambda(self, id, asset, handler, role):
        return lambda_.Function(self, id,
                                code = lambda_.Code.asset(asset),
                                handler = handler,
                                runtime = lambda_.Runtime.PYTHON_3_6,
                                environment = {'first_name': 'omar', 'last_name': 'arif'},
                                role = role
                                )
                            
        
        
    # uses boto3 to create sns topic        
    def create_sns_topic_(self, name):
        sns_client = boto3.client("sns")
        return sns_client.create_topic(Name=name)
    
    # uses boto3 to create sns topic    
    def subscribe_(self, topic, protocol, endpoint):
        sns_client = boto3.client("sns")
        return sns_client.subscribe(TopicArn=topic, Protocol=protocol, Endpoint=endpoint)
        
    # uses boto3 to create alarm
    def create_alarm_(self, sns_topic):
        cw_client = boto3.client("cloudwatch")
        cw_client.put_metric_alarm(
            AlarmName='Skipq_Latency_check',
            ComparisonOperator='GreaterThanThreshold',
            MetricName='latency',
            Dimensions = 
            [{
                'Name': 'SkipQ',
                'Value': 'Request'
            }],
            Namespace = 'NetworkMonitoring',
            Period = 10,
            Threshold = .5,
            EvaluationPeriods=1,
            Statistic='Average',
            AlarmActions=[sns_topic]
            )    