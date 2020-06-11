# from geoip2 import database as geoip_db
import geoip2.database

# reader = geoip_db.Reader('../GeoLite2-City_20200602/GeoLite2-City.mmdb')
reader = geoip2.database.Reader('GeoLite2-City_20200602/GeoLite2-City.mmdb')

def get_location(ip_address):
    if ip_address == None or ip_address == '':
        return {'error': 'Could not geo-locate an empty IP.'}

    response = reader.city(ip_address)

    try:
        city = response.city.name
        country_code = response.country.iso_code
        subdivision = response.subdivisions.most_specific.name

        output = {'city': city,'subdivision': subdivision, 'country_code': country_code}
        #reader.close()
        return output
    except:
        return {'error': 'Could not geo-locate this IP.'}
