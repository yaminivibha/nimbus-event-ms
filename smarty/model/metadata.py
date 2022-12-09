from marshmallow import Schema, fields, post_load

class Metadata(object):
    def __init__(self, record_type, county_fips, county_name, 
                 carrier_route, congressional_district, latitude, 
                 longitude, precision):
        self.record_type = record_type
        self.county_fips = county_fips
        self.county_name = county_name
        self.carrier_route = carrier_route
        self.congressional_district = congressional_district
        self.latitude = latitude
        self.longitude = longitude
        self.precision = precision
    
    def __repr__(self):
      return '<Metadata(name={self.record_type!r})>'.format(self=self)

class MetadataSchema(Schema):
    record_type = fields.Str()
    county_fips = fields.Str()
    county_name = fields.Str()
    carrier_route = fields.Str()
    congressional_district = fields.Str()
    latitude = fields.Number()
    longitude = fields.Number()
    precision = fields.Str()
    
    @post_load
    def get_metadata(self, data, **kwargs):
        return Metadata(**data)