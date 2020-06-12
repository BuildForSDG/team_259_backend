import pytest
from app.user_functions.compute_session_data import generate_location_data

class TestGenerateLocationData(object):
    def test_fake_ip(self):
        test_ip = '239.132.103.156'
        actual = generate_location_data(test_ip)
        expected = {'error': 'Could not geo-locate this IP.'}
        message = 'Expected {}, but got {}'.format(expected, actual)
        assert actual is expected, message

    def test_no_city(self):
        test_ip = '154.114.154.242'
        actual = generate_location_data(test_ip)
        expected = {'ip': test_ip, 'location': 'Somewhere in GH'}
        message = 'Expected {}, but got {}'.format(expected, actual)
        assert actual is expected, message

    def test_real_ipv4(self):
        test_ip = '197.237.27.11'
        actual = generate_location_data(test_ip)
        expected = {'ip': test_ip, 'location': 'Homa Bay, KE'}
        message = 'Expected {}, but got {}'.format(expected, actual)
        assert actual is expected, message

    def test_real_ipv6(self):
        test_ip = '2c0f:fe38:2000:ebff:b0d6:90d8:7d67:66e5'
        actual = generate_location_data(test_ip)
        expected = {'ip': test_ip, 'location': 'Nairobi, KE'}
        message = 'Expected {}, but got {}'.format(expected, actual)
        assert actual is expected, message
