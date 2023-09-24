# aws-list-all-account-resources-by-region-to-csv

It was a Sunday moring and I decided to clean the old resource on my **AWS Account**. For this reason I made this **Python Script**.

The logic is very simple: for each region (regions list) the boto3 client searches the resource (resources list) and create a CSV with the details.

## Configuration

### regions

This list contains all region you want to check

```
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
```

### resources

In this list, I added only my resources type. If you need other resource, you can add in this list and after implement the specific logic

```
resources = [
    'ec2',
    's3',
    'sns',
    'dynamodb',
    'lambda',
    'apigateway',
    'logs',
    'events'
]
```

### csv configuration

If you add/ remove columns in **csv_header** please change also **generate_output_line** method

```
csv_delimiter = '|' # Delimiter used in the CSV file
csv_header = [ 'Region' , 'ResourceType','ResourceName']
csv_quoting = csv.QUOTE_MINIMAL
```

## Output

In the following lines, you can see an example from my subscription

```
Region|ResourceType|ResourceName
eu-central-1|dynamodb|first_table_id
eu-central-1|lambda|first_lambda_id
eu-central-1|apigateway|first_apigateway_id
eu-central-1|logs|/aws/lambda/first_lambda_id
```

## Follow Me

- [AndreaCarratta@Linkedin](https://links.devandreacarratta.it/linkedin)
- [BugsInCloud@YouTube](https://links.devandreacarratta.it/youtube)
- [AndreaCarratta@HomePage](https://devandreacarratta.it/)
- [AndreaCarratta@Blog](https://blog.devandreacarratta.it/)
