import json, smarty_response_contract as smarty_response

from flask import Flask, Response, request
from flask_cors import CORS
from datetime import datetime
from types import SimpleNamespace

from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup

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
    # Credentials
    AUTH_ID = "b0520535-17f6-c6f3-cbec-947c6d20a18b"
    AUTH_TOKEN = "cZ8kepXKvo3y7fhi2eFI"
    credentials = StaticCredentials(AUTH_ID, AUTH_TOKEN)
    print("Smarty credentials HERE: ")
    print(credentials)
    client = ClientBuilder(credentials).with_licenses(
        ["us-core-cloud"]).build_us_street_api_client()

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
    print("There is at least one candidate.")
    print("If the match parameter is set to STRICT, the address is valid.")
    print("Otherwise, check the Analysis output fields to see if the address is valid.\n")
    print("ZIP Code: " + first_candidate.components.zipcode)
    print("County: " + first_candidate.metadata.county_name)
    print("Latitude: {}".format(first_candidate.metadata.latitude))
    # Complete list of output fields is available here:  https://smartystreets.com/docs/cloud/us-street-api#http-response-output
    
    content = json.dumps(first_candidate)
    print(content)
    content_address = json.loads(content, object_hook=lambda d: SimpleNamespace(**d))
    return content_address
"""
    if result:
        response = Response(json.dumps(result), status=200,
                            content_type=CONTENT_TYPE_JSON)
    else:
        response = Response("NOT FOUND", status=404,
                            content_type=CONTENT_TYPE_PLAIN_TEXT)
"""

def encode_complex(z):
    if isinstance(z, complex):
        return (z.real, z.imag)
    else:
        type_name = z.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5020, debug=False)
    #app.run(host='localhost', port=5020, debug=True)
    #app.run(host="0.0.0.0", port=5012, debug=True)