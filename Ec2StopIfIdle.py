import boto3
import datetime

def lambda_handler(event, context):
    # Specify the region that your instances are running in
    ec2 = boto3.client('ec2', region_name='us-east-1')

    # Calculate the time threshold for idle instances (in minutes)
    idle_time_threshold = 30
    threshold_time = datetime.datetime.now() - datetime.timedelta(minutes=idle_time_threshold)

    # Use the describe_instances() method to get information about all instances
    response = ec2.describe_instances()

    # Create a list of idle instances
    instances_to_stop = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # Check if the instance is in the "running" state and has a "LastUse" tag
            if instance['State']['Name'] == 'running' and 'Tags' in instance:
                last_use_tag = next((tag for tag in instance['Tags'] if tag['Key'] == 'LastUse'), None)
                if last_use_tag:
                    last_use_time = datetime.datetime.strptime(last_use_tag['Value'], '%Y-%m-%d %H:%M:%S')
                    # Check if the instance has been idle for more than the threshold time
                    if last_use_time < threshold_time:
                        instances_to_stop.append(instance['InstanceId'])

    # Stop the instances
    if instances_to_stop:
        ec2.stop_instances(InstanceIds=instances_to_stop)
        print('Stopped instances: ' + ', '.join(instances_to_stop))
    else:
        print('No idle instances found.')

    return {
        'statusCode': 200,
        'body': 'Stopped instances: ' + ', '.join(instances_to_stop)
    }