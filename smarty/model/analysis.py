from marshmallow import Schema, fields, post_load

class Analysis(object):
    def __init__(self, dpv_match_code, dpv_footnotes, 
                 dpv_cmra, dpv_vacant, dpv_no_stat,
                 ews_match, footnotes, lacslink_indicator,
                 suitelink_match, enhanced_match):
        self.dpv_match_code = dpv_match_code
        self.dpv_footnotes = dpv_footnotes
        self.dpv_cmra = dpv_cmra
        self.dpv_vacant = dpv_vacant
        self.dpv_no_state = dpv_no_stat
        self.ews_match = ews_match
        self.footnotes = footnotes
        self.lacslink_indicator = lacslink_indicator
        self.suitelink_match = suitelink_match
        self.enhanced_match = enhanced_match
    
    def __repr__(self):
        print(self)
    
class AnalysisSchema(Schema):
    dpv_match_code = fields.Str()
    dpv_footnotes = fields.Str()
    dpv_cmra = fields.Str()
    dpv_vacant = fields.Str()
    dpv_no_stat = fields.Str()
    active = fields.Str()
    ews_match = fields.Bool()
    footnotes = fields.Str()
    lacslink_indicator = fields.Str()
    suitelink_match = fields.Str()
    enhanced_match = fields.Str()
    
    @post_load
    def get_analysis(self, data, **kwargs):
        return Analysis(**data)