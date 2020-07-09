import boto3
import json
import os

def toggle_instances(region, action, instances):
    session = boto3.Session(
        region_name=region
    )

    client = session.client('ec2')
    
    response = 'None'
    if action == 'start':
        response = client.start_instances(InstanceIds=instances)
    elif action == 'stop':
        response = client.stop_instances(InstanceIds=instances) 
    else:
        print('Action not supported. Must be start or stop')
        
    print(response)
    return response
    
def lambda_handler(event, context):

    toggle_instances('sa-east-1', os.environ['action'], ['i-087b4f88e3633dfd2', 'i-02d0ef71d54f954b0'], )
    toggle_instances('us-west-2', os.environ['action'], ['i-0f39d9b1d0ae87e78', 'i-046c4cf1a9acf8290', 'i-02b2bb9f6310b9ebb','i-043cbe361b0a7ac67'])
    
    rtnmsg = 'Completed Instances action of: ' + os.environ['action']
    return {'status': rtnmsg}