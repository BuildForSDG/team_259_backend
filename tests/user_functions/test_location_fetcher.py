import pytest
from app.user_functions.location_fetcher import get_location

class TestGetLocation(object):

    def test_empty_ip(self):
        test_ip= ''
        actual = get_location(test_ip)
        expected = {'error': 'Could not geo-locate an empty IP.'}
        message = 'Expected {}, but got {}'.format(expected, actual)
        assert actual is expected, message 

    def test_real_ip_nairobi(self):
        test_ip = '102.68.77.26'
        actual = get_location(test_ip)
        expected = {'city': 'Nairobi', 'subdivision': 'Nairobi Province', 'country_code': 'KE'}
        message = 'Expected {}, but got {}'.format(expected, actual)
        assert actual is expected, message

    def test_fake_ip(self):
        test_ip = '239.132.103.156'
        actual = get_location(test_ip)
        expected = {'error': 'Could not geo-locate this IP.'}
        message = 'Expected {}, but got {}'.format(expected, actual)
        assert actual is expected, message
     