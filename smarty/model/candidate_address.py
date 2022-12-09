from marshmallow import post_load, Schema, fields
from .components import Components, ComponentsSchema
from .metadata import Metadata, MetadataSchema
from .analysis import Analysis, AnalysisSchema

class CandidateAddress(object):
    def __init__(self, input_index, candidate_index, delivery_line_1, 
                 last_line, delivery_point_barcode,
                 Components, Metadata, Analysis):
        self.input_index = input_index
        self.candidate_index = candidate_index
        self.delivery_line_1 = delivery_line_1
        self.last_line = last_line
        self.delivery_point_barcode = delivery_point_barcode
        super(CandidateAddress, self).__init__(Components)
        super(CandidateAddress, self).__init__(Metadata)
        super(CandidateAddress, self).__init__(Analysis)
        
    def __repr__(self):
        return '<CandidateAddress(name={self.input_index!r})>'.format(self=self)
    
class CandidateAddressSchema(Schema):
    input_index = fields.Number()
    candidate_index = fields.Number()
    delivery_line_1 = fields.Str()
    last_line = fields.Str()
    delivery_point_barcode = fields.Str()
    #@post_load

'''
class Components:
    primary_number = str,
    street_name = str,
    street_suffix = str,
    city_name = str,
    state_abbreviation = str,
    zipcode = str,
    plus4_code = str,
    delivery_point = str,
    delivery_point_check_digit = str,

class Metadata:
    record_type = str,
    county_fips = str,
    county_name = str,
    carrier_route = str,
    congressional_district = str,
    latitude = float,
    longitude = float,
    precision = str,

class Analysis:
    dpv_match_code = str,
    dpv_footnotes = str,
    dpv_cmra = str,
    dpv_vacant = str,
    ews_match = bool,
    footnotes = str, 
'''