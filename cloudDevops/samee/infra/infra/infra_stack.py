#importing required packages
from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk import aws_sns_subscriptions as subscriptions
from aws_cdk import aws_sns as sns
from aws_cdk import aws_cloudwatch_actions as cw_actions
from aws_cdk import aws_events, aws_events_targets, aws_iam 

#from aws_cdk import aws_dynamodb as dynamodb


import os.path
dirname=os.path.dirname(__file__)


class InfraStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        
        #Creating role to be used by lambda that enables policies needed to run stack
        lambda_role = self.create_lambda_role()
        
        
        #Creating lambda that publishes metrices related to website's health: latency, availability
        hw_lambda = self.create_lambda('metricPublisher', './lambda', 'metric_publisher.publish_metric', lambda_role)
        
        
        # Scheduling lambda to run periodically every minute 
        lambda_schedule = aws_events.Schedule.rate(core.Duration.minutes(1))
        event_lambda_target = aws_events_targets.LambdaFunction(handler = hw_lambda)
        lambda_cw_event = aws_events.Rule(self, "hw_lambda_rule", description="Periodic Lambda", 
        enabled =True, schedule = lambda_schedule, targets=[event_lambda_target])
        
        
        #Creating cloudwatch  metric for use inside cloudwatch alarm to track website latency
        metric_latency = cloudwatch.Metric(
        namespace="SameeSkipQMonitoring",
        metric_name="LatencyInSeconds",
        dimensions=dict(skipq_webpage="latency_performance")
        )

        #Creating cloudwatch  metric for use inside cloudwatch alarm to track website availability
        metric_availability = cloudwatch.Metric(
        namespace="SameeSkipQMonitoring",
        metric_name="IsWebsiteDown",
        dimensions=dict(skipq_webpage="is_website_down"),
        statistic="Maximum"
        )       
        
        #Creating cloudwatch Alarm that activates when latency goes above threshold of 0.5s
        alarm_latency = cloudwatch.Alarm(self, "AlarmLatency",
            metric=metric_latency,
            threshold=0.5,
            evaluation_periods=1,
            datapoints_to_alarm=1,
            comparison_operator = cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD
        )
        
        #Creating cloudwatch Alarm that activates when website goes down
        alarm_availability = cloudwatch.Alarm(self, "AlarmAvailability",
            metric=metric_availability,
            threshold=0,
            evaluation_periods=1,
            datapoints_to_alarm=1,
            comparison_operator = cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD
        )        
        
        
        #Creating Simple Notification Service (SNS) to notify via email when latency or availability alarms are on.. 
        topic = sns.Topic(self, "SameeSkipQWebHealth")
        topic.add_subscription(subscriptions.EmailSubscription("samee@skipq.org"))
        alarm_latency.add_alarm_action(cw_actions.SnsAction(topic))
        alarm_availability.add_alarm_action(cw_actions.SnsAction(topic))
        

    def create_lambda_role(self):
        #create_lambda_role: assigns lambda rol along with IAM serviceprincipal and required policies
        lambdaRole = aws_iam.Role(self, "lambda_role", 
        assumed_by = aws_iam.ServicePrincipal("lambda.amazonaws.com"),
        managed_policies = [
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess")     
            ])
        return lambdaRole
        
    def create_lambda(self, id, asset, handler, role):
        #Creates lambda using the hanlder specified inside asset using role specified by role.  
        return lambda_.Function(self, id,
        code=lambda_.Code.asset(asset),
        handler=handler,
        runtime=lambda_.Runtime.PYTHON_3_6, 
        environment = {'webpage': "https://www.skipq.org"
            },
            role=role
        )