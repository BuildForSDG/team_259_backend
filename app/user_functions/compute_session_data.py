from flask import request

from user_functions.platform_fetcher import compute_platform_version
from user_functions.location_fetcher import get_location


def generate_device_data(user_agent):
    user_agent_platform = request.user_agent.platform
    device_os = compute_platform_version(user_agent, user_agent_platform)
    if device_os is None:
        return{'error': 'This request has been rejected. Please use a recognised device'}
    return {'device_os': device_os}

def generate_location_data(ip):    
    location = get_location(ip)
    if 'error' in location.keys():
        return{'error':location['error']}
    if location['city'] is None and location['country_code'] is None:
        return{'error':'Could not compute devoce location.'}
    if location['city'] is None  and location['country_code'] is not None:
        return {'ip': ip, 'location':'Somewhere in {}'.format(location['country_code'])}
    return {'ip': ip, 'location':'{} ,{}'.format(location['city'], location['country_code'])}
        
    # # Get User-agent and ip address, then compute operating system
    # my_ip = request.environ.get('HTTP_X_FORWARDED_FOR')
    # if my_ip is None:
    #     ip = request.environ['REMOTE_ADDR']
    # else:
    #     ip = request.environ['HTTP_X_FORWARDED_FOR']

    # location = get_location(ip)
    # if location['error']:
    #     abort(400, location['error'])
    # if location['city'] is None and location['country_code'] is None:
    #     abort(400, 'Could not compute device location.')

    # user_agent = str(request.user_agent)
    # user_agent_platform = request.user_agent.platform
    # device_os = compute_platform_version(user_agent, user_agent_platform)
    # if device_os is None or ip is None:
    #     abort(400, 'This request has been rejected. Please use a recognised device')
