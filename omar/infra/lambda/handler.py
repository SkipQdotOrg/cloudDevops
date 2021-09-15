import os
def lambda_handler(event, context):
    message = 'Hello {} {}!'.format(os.environ.get('first_name'), os.environ.get('last_name'))
    print(message)
    return {'message': message}