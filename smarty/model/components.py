from marshmallow import Schema, fields, post_load

class Components(object):
    def __init__(self, primary_number, street_name, street_suffix, 
                 city_name, state_abbreviation, zipcode, plus4_code, 
                 delivery_point, delivery_point_check_digit):
        self.primary_number = primary_number
        self.street_name = street_name
        self.street_suffix = street_suffix
        self.city_name = city_name
        self.state_abbreviation = state_abbreviation
        self.zipcode = zipcode
        self.plus4_code = plus4_code
        self.delivery_point = delivery_point
        self.delivery_point_check_digit = delivery_point_check_digit
        
    def __repr__(self):
        return '<Components(name={self.primary_number!r})>'.format(self=self)
      
class ComponentsSchema(Schema):
    primary_number = fields.Str()
    street_name = fields.Str()
    street_suffix = fields.Str()
    city_name = fields.Str()
    state_abbreviation = fields.Str()
    zipcode = fields.Str()
    plus4_code = fields.Str()
    delivery_point = fields.Str()
    delivery_point_check_digit = fields.Str()
    
    @post_load
    def get_components(self, data, **kwargs):
        return Components(**data)