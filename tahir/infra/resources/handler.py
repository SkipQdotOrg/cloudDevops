import os

def lambda_handler(event, context):
    message = 'Hello {} {}!'.format(os.environ.get('first_name'), os.environ.get('last_name'))
    print(os.environ.get('first_name'))
    print("here you go.")
    print(os.environ.get('AWS_REGION'))
    return { 
        'message' : message
    }