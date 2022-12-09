import json
from flask import Flask, request, Response
from flask_cors import CORS
from pprint import pprint
from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup
from model.candidate import CandidateSchema

application = app = Flask(__name__)
CORS(app)

# TODO: Add caching

# TODO: store these constants in a shared file
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_PLAIN_TEXT = "text/plain"

# TODO: add middleware to check if requestor is authorized to make this call
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

@app.route("/smarty/", methods=["POST"])
def verify_address_freeform():

    # TODO: store these credentials in AWS KMS
    AUTH_ID = "b0520535-17f6-c6f3-cbec-947c6d20a18b"
    AUTH_TOKEN = "cZ8kepXKvo3y7fhi2eFI"
    credentials = StaticCredentials(AUTH_ID, AUTH_TOKEN)
    client = ClientBuilder(credentials).with_licenses(
        ["us-core-cloud"]).build_us_street_api_client()
    
    # TODO: decision - keep freeform?
    street = request.json['street']
    print(f'Input is: {street}')
    lookup = StreetLookup()
    lookup.street = street

    try:
        client.send_lookup(lookup)
    except exceptions.SmartyException as err:
        print(err)
        return

    result = lookup.result

    if not result:
        print("No candidates. This means the address is not valid.")
        return "Address not found", 404 

    first_candidate = result[0]
    pprint(vars(first_candidate))
    schema_candidate = CandidateSchema(many=False)
    result_candidate = schema_candidate.dump(first_candidate)
    print("Results for result_candidate: ")
    pprint(result_candidate)
    print("\n")
    result = Response(json.dumps(result_candidate), status=200,
                      content_type="application/json")
    return result

if __name__ == '__main__':
    app.run(host='localhost', port=5020, debug=False)