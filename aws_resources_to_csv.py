import boto3
import os
import csv

# Fill this list with the regions you want to export
regions =  [
    'us-east-2','us-east-1',
    'us-west-1','us-west-2',
    'af-south-1',
    'ap-east-1',
    'ap-south-1', 'ap-south-2',
    'ap-southeast-1','ap-southeast-2','ap-southeast-3','ap-southeast-4',
    'ap-northeast-1','ap-northeast-3','ap-northeast-2',
    'ca-central-1',
    'eu-central-1','eu-central-2',
    'eu-west-1','eu-west-2','eu-west-3',
    'eu-south-1','eu-south-2',
    'eu-north-1',
    'il-central-1',
    'me-south-1',
    'me-central-1',
    'sa-east-1'
]

# Fill this list with the resources you want to export
resources = ['ec2', 's3', 'sns', 'dynamodb', 'lambda', 'apigateway', 'logs', 'events']

csv_delimiter = '|' # Delimiter used in the CSV file
csv_header = [ 'Region' , 'ResourceType','ResourceName']
csv_quoting = csv.QUOTE_MINIMAL 

csv_lines = []

def generate_output_line(awsRegion, awsType, awsName):
    csv_line = [awsRegion, awsType, awsName]
    csv_lines.append(csv_line)

def get_ec2_instance_ids(session, region):
    ec2_client = session.client('ec2', region_name=region)
    response = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['NomeRisorsa']}])
    return [instance['InstanceId'] for reservation in response.get('Reservations', []) for instance in reservation.get('Instances', [])]

def get_s3_bucket_ids(session, region):
    s3_client = session.client('s3', region_name=region)
    response = s3_client.list_buckets()
    return [bucket['Name'] for bucket in response['Buckets']]

def get_sns_topic_ids(session, region):
    sns_client = session.client('sns', region_name=region)
    response = sns_client.list_topics()
    return [topic['TopicArn'] for topic in response.get('Topics', [])]

def get_dynamodb_table_names(session, region):
    dynamodb_client = session.client('dynamodb', region_name=region)
    response = dynamodb_client.list_tables()
    return response['TableNames']

def get_lambda_function_names(session, region):
    lambda_client = session.client('lambda', region_name=region)
    response = lambda_client.list_functions()
    return [function['FunctionName'] for function in response['Functions']]

def get_apigateway_api_names(session, region):
    apigateway_client = session.client('apigateway', region_name=region)
    response = apigateway_client.get_rest_apis()
    return [api['name'] for api in response['items']]

def get_logs_log_groups(session, region):
    logs_client = session.client('logs', region_name=region)
    response = logs_client.describe_log_groups()
    return [log_group['logGroupName'] for log_group in response['logGroups']]

def get_events_rule_names(session, region):
    events_client = session.client('events', region_name=region)
    response = events_client.list_rules()
    return [rule['Name'] for rule in response['Rules']]

for region in regions:
    session = boto3.Session(region_name=region)
    for resource_type in resources:
        try:
            print('Resource Type:', resource_type)
            if resource_type == 'ec2':
                instance_ids = get_ec2_instance_ids(session, region)
                for instance_id in instance_ids:
                    generate_output_line(region,resource_type, instance_id)
            elif resource_type == 's3':
                bucket_ids = get_s3_bucket_ids(session, region)
                for bucket_id in bucket_ids:
                    generate_output_line(region,resource_type, bucket_id)
            elif resource_type == 'sns':
                topic_ids = get_sns_topic_ids(session, region)
                for topic_id in topic_ids:
                    generate_output_line(region,resource_type, topic_id)
            elif resource_type == 'dynamodb':
                table_names = get_dynamodb_table_names(session, region)
                for table_name in table_names:
                    generate_output_line(region,resource_type, table_name)
            elif resource_type == 'lambda':
                function_names = get_lambda_function_names(session, region)
                for function_name in function_names:
                    generate_output_line(region,resource_type, function_name)
            elif resource_type == 'apigateway':
                api_names = get_apigateway_api_names(session, region)
                for api_name in api_names:
                    generate_output_line(region,resource_type, api_name)
            elif resource_type == 'logs':
                log_groups = get_logs_log_groups(session, region)
                for log_group in log_groups:
                    generate_output_line(region,resource_type, log_group)
            elif resource_type == 'events':
                rule_names = get_events_rule_names(session, region)
                for rule_name in rule_names:
                    generate_output_line(region,resource_type, rule_name)           
            else:
                generate_output_line(region,resource_type, 'Not Implemented')
        except:
            generate_output_line(region,resource_type, 'Exception')

baseDirectoryPath = os.path.dirname(os.path.realpath(__file__))

output_file_name = f"{baseDirectoryPath}/output.csv"

with open("output.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=csv_delimiter, quoting=csv_quoting)
    csvwriter.writerows(csv_lines)

print('Output file generated:', output_file_name)