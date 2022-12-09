from marshmallow import Schema, fields, post_load
from .components import ComponentsSchema
from .metadata import MetadataSchema
from .analysis import AnalysisSchema

class Candidate(object):
    def __init__(self, addressee, input_id, input_index, 
                 candidate_index, delivery_line_1, delivery_line_2,
                 last_line, delivery_point_barcode):
        self.addressee = addressee
        self.input_id = input_id
        self.input_index = input_index
        self.candidate_index = candidate_index
        self.delivery_line_1 = delivery_line_1
        self.delivery_line_2 = delivery_line_2
        self.last_line = last_line
        self.delivery_point_barcode = delivery_point_barcode
        #self.components = Components
        #self.metadata = MetaData
        #self.analysis = Analysis
        
    def __repr__(self):
        return '<CandidateAddress(name={self.input_index!r})>'.format(self=self)
    
class CandidateSchema(Schema):
    input_id = fields.Number()
    input_index = fields.Number()
    candidate_index = fields.Number()
    addressee = fields.Str()
    delivery_line_1 = fields.Str()
    delivery_line_2 = fields.Str()
    last_line = fields.Str()
    delivery_point_barcode = fields.Str()
    components = fields.Nested(ComponentsSchema)
    metadata = fields.Nested(MetadataSchema)
    analysis = fields.Nested(AnalysisSchema)
    
    @post_load
    def get_candidate(self, data, **kwargs):
        return Candidate(**data)