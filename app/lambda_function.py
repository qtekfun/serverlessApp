# lambda_function.py

import json, tempfile, boto3, os, logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Retrieve environment variables
s3_bucket_name = os.environ['S3_BUCKET_NAME']

def lambda_handler(event, context):

    logging.info(f"Received event: {json.dumps(event)}")
    
    s3_url = upload_to_s3()

    # Extract the parameter from the incoming JSON request
    try:
        request_body = json.loads(event['body'])
        parameter_value = request_body.get('parameter', 'unknown')
    except json.JSONDecodeError:
        parameter_value = 'unknown'

    # Construct the response body including the parameter value
    response_body = f"Hello, I'm fine. Your env vars are {s3_bucket_name}.\n"
    response_body += f"The parameter you sent me was {parameter_value}\n"
    response_body += f"event is {event}\n"
    response_body += f"{s3_url}"

    # Return the response with a 200 status code
    return {
        'statusCode': 200,
        'body': response_body
    }

def upload_to_s3():

    json_data = {"key": "value"}

    # with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
    #     json.dump(json_data, temp_file)

    # s3 = boto3.client('s3')
    # s3_key = 'top.json'

    # with open(temp_file.name, 'rb') as data:
    #     s3.upload_file(data, s3_bucket_name, s3_key)

    # try:
    #     response = s3.generate_presigned_url('get_object',
    #                                         Params={'Bucket': s3_bucket_name,
    #                                                 'Key': s3_key},
    #                                         ExpiresIn=600)
    # except ClientError as e:
    #     logging.error(e)
    #     return None
    json_data = {"key": "value"}

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        json.dump(json_data, temp_file)

    s3 = boto3.client('s3')
    s3_key = 'top.json'

    with open(temp_file.name, 'rb') as data:
        s3.upload_fileobj(data, s3_bucket_name, s3_key)

    s3_url = f'https://{s3_bucket_name}.s3.amazonaws.com/{s3_key}'
    print(f'Archivo JSON subido a S3: {s3_url}')

    return s3_url
