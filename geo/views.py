import json
from urllib import urlencode
from urllib2 import urlopen

from django.conf import settings
from django.http import HttpResponse

BBOX = {
    'top': 40.922,
    'right': -73.71,
    'bottom': 40.495,
    'left': -74.293
}

def geocode(request):
    result = None
    location = request.GET.get('location', None)
    if location:
        result = _geocode_with_yahoo(location)
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps(result))
    return response            

def _is_in_bbox(latitude, longitude):
    return ((latitude <= BBOX['top'] and latitude >= BBOX['bottom']) and 
        (longitude <= BBOX['right'] and longitude >= BBOX['left']))

def _geocode_with_yahoo(location):
    """
    Geocode using Yahoo Placefinder. Return None if no results are found within
    BBOX.
    """
    query = {
        'location': location,
        'flags': 'CJ',
        'count': 5,
        'appid': settings.YAHOO_APP_ID,
    }
    url = 'http://where.yahooapis.com/geocode?' + urlencode(query)
    best_result = None
    try:
        results = json.load(urlopen(url))
        for result in results['ResultSet']['Results']:
            if _is_in_bbox(float(result['latitude']), float(result['longitude'])):
                if not best_result or best_result['quality'] < result['quality']:
                    best_result = result
    except:
        pass

    if best_result:
        return {
            'latitude': best_result['latitude'],
            'longitude': best_result['longitude'],
        }
    return None
