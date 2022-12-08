class CandidateAddress:
    input_index = int,
    candidate_index = int,
    delivery_line_1 = str,
    last_line = str,
    delivery_point_barcode = str,
    components = object,
    metadata = object,
    analysis = object,

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