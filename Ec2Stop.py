import boto3

def lambda_handler(event, context):
    # Specify the region that your instances are running in
    ec2 = boto3.client('ec2', region_name='us-east-1')

    # Use the describe_instances() method to get information about all running instances
    response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

    # Create a list of running instances
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance['InstanceId'])

    # Stop the instances
    if instances:
        ec2.stop_instances(InstanceIds=instances)
        print('Stopped instances: ' + ', '.join(instances))
    else:
        print('No instances found in "running" state.')

    return {
        'statusCode': 200,
        'body': 'Stopped instances: ' + ', '.join(instances)
    }