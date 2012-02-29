import os
from django.contrib.gis.utils import LayerMapping
from models import School

# shp fields:
['ATS_CODE', 'BORO', 'BORONUM', 'LOC_CODE', 'SCHOOLNAME', 'SCH_TYPE', 'MANAGED_BY', 'GEO_DISTRI', 'ADMIN_DIST', 'ADDRESS', 'STATE_CODE', 'ZIP', 'PRINCIPAL', 'PRIN_PH', 'FAX', 'GRADES', 'City']

# shp field types:
['OFTString', 'OFTString', 'OFTReal', 'OFTString', 'OFTString', 'OFTString', 'OFTReal', 'OFTInteger', 'OFTReal', 'OFTString', 'OFTString', 'OFTInteger', 'OFTString', 'OFTString', 'OFTString', 'OFTString', 'OFTString']


school_mapping = {
    'borough': 'BORO',
    'name': 'SCHOOLNAME',
    'type': 'SCH_TYPE',
    'geo_district': 'GEO_DISTRI',
    'admin_district': 'ADMIN_DIST',
    'address': 'ADDRESS',
    'state': 'STATE_CODE',
    'zip_code': 'ZIP',
    'grades': 'GRADES',
    'city': 'City',
    'point': 'POINT',
}

school_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/Public_School_Locations/Public_Schools_Points_2011-2012A.shp'))

def run(verbose=True):
    lm = LayerMapping(School, school_shp, school_mapping, transform=True, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)
