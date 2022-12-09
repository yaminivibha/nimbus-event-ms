import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from types import SimpleNamespace
from pprint import pprint

from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup

#from model.candidate_address import CandidateAddress, CandidateAddressSchema
from model.candidate import Candidate, CandidateSchema
from model.components import Components, ComponentsSchema
from model.metadata import MetadataSchema
from model.analysis import AnalysisSchema

# Create the Flask application object.
app = Flask(__name__)
CORS(app)

"""
application2 = app = Flask(__name__, 
                           static_url_path='/smarty/', 
                           static_folder='static/class-ui/', 
                           template_folder='web/templates')
CORS(application2)
"""


"""
TODO: Add Middleware
- @before_request : social login OIDC IAM GOOGL,
- @after_request 

@app.before_request
def before_request_func():
    print("BEFORE_REQUEST executing!")
    print("Request = ", json.dumps(request, indent=2, default=str))

@app.after_request
def after_request_func():
    print("AFTER_REQUEST executing!")
    print("Request = ", json.dumps(response, indent=2, default=str))
    sns_middleware.check_publish(request, response)
    return response

"""
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_PLAIN_TEXT = "text/plain"


@app.route("/smarty/", methods=["POST"])
def verify_address():
    # TODO: store these credentials in AWS KMS
    AUTH_ID = "b0520535-17f6-c6f3-cbec-947c6d20a18b"
    AUTH_TOKEN = "cZ8kepXKvo3y7fhi2eFI"
    credentials = StaticCredentials(AUTH_ID, AUTH_TOKEN)
    client = ClientBuilder(credentials).with_licenses(
        ["us-core-cloud"]).build_us_street_api_client()
    
    # TODO: create request with user input
    # print(f'Input is: {address}')
    # lookup = StreetLookup()
    # lookup.street = address.street

    # Documentation for input fields can be found at:
    # https://smartystreets.com/docs/us-street-api#input-fields
    lookup = StreetLookup()
    lookup.input_id = "24601"  # Optional ID from your system
    lookup.addressee = "John Doe"
    lookup.street = "1600 Amphitheatre Pkwy"
    lookup.street2 = "closet under the stairs"
    lookup.secondary = "APT 2"
    lookup.urbanization = ""  # Only applies to Puerto Rico addresses
    lookup.city = "Mountain View"
    lookup.state = "CA"
    lookup.zipcode = "94043"
    lookup.candidates = 3
    lookup.match = "invalid"  # "invalid" is the most permissive match,
    # this will always return at least one result even if the address is invalid.
    # Refer to the documentation for additional Match Strategy options.

    try:
        client.send_lookup(lookup)
    except exceptions.SmartyException as err:
        print(err)
        return

    result = lookup.result

    if not result:
        print("No candidates. This means the address is not valid.")
        return

    first_candidate = result[0]
    pprint(vars(first_candidate))
    schema_candidate = CandidateSchema(many=False)
    result_candidate = schema_candidate.dump(first_candidate)
    print("Results for result_candidate: ")
    pprint(result_candidate)
    print("\n")
    content = jsonify(result_candidate)
    return content

"""
    print("There is at least one candidate.")
    print("If the match parameter is set to STRICT, the address is valid.")
    print("Otherwise, check the Analysis output fields to see if the address is valid.\n")
    print("ZIP Code: " + first_candidate.components.zipcode)
    print("County: " + first_candidate.metadata.county_name)
    print("Latitude: {}".format(first_candidate.metadata.latitude))
    # Complete list of output fields is available here:  https://smartystreets.com/docs/cloud/us-street-api#http-response-output
    print("\n")
    
    #pprint(vars(first_candidate.analysis))
    schema_analysis = AnalysisSchema(many=False)
    result_analysis = schema_analysis.dump(first_candidate.analysis)
    print("Results for result_analysis: ")
    pprint(result_analysis)
    print("\n")
    
    #pprint(vars(first_candidate.metadata))
    schema_metadata = MetadataSchema(many=False)
    result_metadata = schema_metadata.dump(first_candidate.metadata)
    print("Results for result_metadata: ")
    pprint(result_metadata)
    print("\n")
    
    #pprint(vars(first_candidate.components))
    schema_components = ComponentsSchema(many=False)
    result_components = schema_components.dump(first_candidate.components)
    print("Results for result_components: ")
    pprint(result_components)
    print("\n")
"""

def encode_complex(z):
    if isinstance(z, complex):
        return (z.real, z.imag)
    else:
        type_name = z.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable")

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5020, debug=False)
    app.run(host='localhost', port=5020, debug=False)
    #app.run(host="0.0.0.0", port=5012, debug=True)