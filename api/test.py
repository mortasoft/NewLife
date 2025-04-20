import utils as app_utils

result = { 'message': 'Data retrieved successfully.', 'status_code': 200, 'result': 'success', 'data': 'data' }

print(app_utils.generate_message(result['data'], 'create'))