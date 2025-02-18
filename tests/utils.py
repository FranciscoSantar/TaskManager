
from flask import Response
from datetime import datetime

def format_date_in_response(response:Response)->dict:
    response_data = response.json
    if isinstance(response_data['data'], list):
        for data_task in response_data['data']:
            for key in ['created_at', 'updated_at']:
                data_task[key] = datetime.strptime(data_task[key], '%a, %d %b %Y %H:%M:%S GMT')
    else:
        for key in ['created_at', 'updated_at']:
            response_data['data'][key] = datetime.strptime(response_data['data'][key], '%a, %d %b %Y %H:%M:%S GMT')
    return response_data