import boto3
import os

# set ec2_tag=shoutcast
# set region_list=sa-east-1,us-west-2
# set action=start


def toggle_instances(region, toggle_action, instances):

    session = boto3.Session(
        region_name=region
    )

    client = session.client('ec2')
    
    response = 'None'
    if toggle_action == 'start':
        response = client.start_instances(InstanceIds=instances)
    elif toggle_action == 'stop':
        response = client.stop_instances(InstanceIds=instances) 
    else:
        print('Action not supported. Must be start or stop')
        
    print(response)
    return response


def get_instance_list(region, tag_name):

    instance_list = []

    session = boto3.Session(
        region_name=region
    )

    ec2 = session.resource('ec2')

    instances = ec2.instances.filter(Filters=[{
        'Name': 'tag:'+tag_name,
        'Values': ['*']}])

    for instance in instances:
        instance_list.append(instance.id)

    print(instance_list)
    return instance_list


def run_now():

    ec2_tag = os.environ.get("ec2_tag")  # any ec2 tag name
    region_list = os.environ.get("region_list").split(",")  # comma-delimited value e.g us-east-1,us-east-2
    action = os.environ['action']  # start/stop

    for region in region_list:
        this_list = get_instance_list(region, ec2_tag)
        if this_list:
            toggle_instances(region, action, this_list)
        else:
            print('no instances found with specified tag')


def lambda_handler(event, context):

    run_now()

    return_message = 'Completed Instances action of: ' + action
    return {'status': return_message}


def main():

    run_now()

    return_message = 'Completed Instances action of: ' + action
    print(return_message)


if __name__ == '__main__': main()