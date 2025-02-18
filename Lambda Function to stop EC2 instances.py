import boto3
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

region = 'us-east-1'

def lambda_handler(event, context):
    try:
        ec2_resource = boto3.resource("ec2", region_name=region)

        # Filter running instances
        instances = list(ec2_resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]))
        logger.info(f"EC2 region: {region}")
        logger.info(f"{len(instances)} instances running.")

        if not instances:
            return "No running instances found."

        instance_ids = []
        for instance in instances:
            instance_name = next((tag['Value'] for tag in instance.tags if tag['Key'] == 'Name'), "Unknown")
            logger.info(f"Instance ID: {instance.id}, Name: {instance_name}")
            instance_ids.append(instance.id)

        # Stop all instances in a single API call
        ec2_resource.instances.filter(InstanceIds=instance_ids).stop()
        logger.info(f"Stopping instances: {instance_ids}")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return str(e)

    return f"Stopped instances: {instance_ids}"
