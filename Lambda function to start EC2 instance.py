import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='us-east-1')  # Change the region if needed

    # Get all stopped instances with a specific tag (optional)
    filters = [
        {'Name': 'tag:AutoShutdown', 'Values': ['true']},
        {'Name': 'instance-state-name', 'Values': ['stopped']}
    ]

    instances = ec2.describe_instances(Filters=filters)

    instance_ids = [instance["InstanceId"] for reservation in instances["Reservations"] for instance in reservation["Instances"]]

    if instance_ids:
        ec2.start_instances(InstanceIds=instance_ids)
        print(f"Started instances: {instance_ids}")
    else:
        print("No stopped instances found to start.")

    return {"status": "Success", "started_instances": instance_ids}
