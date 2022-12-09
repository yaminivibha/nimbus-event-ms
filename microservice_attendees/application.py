from flask import Flask, Response, request
from datetime import datetime
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from nimbus_attendees import Nimbus_Attendees
from flask_cors import CORS
import json

# Create the Flask application object.
application = app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')
CORS(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/db_name'
#db = SQLAlchemy(app)
#ma = Marshmallow(app)

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

CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_PLAIN_TEXT = "text/plain"


@app.get("/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "Microservice_attendees",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    response = Response(json.dumps(msg), status=200,
                        content_type=CONTENT_TYPE_JSON)
    return response


@app.route("/attendees/<uid>", methods=["GET"])
def get_attendee_by_uid(uid):
    result = Nimbus_Attendees.get_by_uid(uid)
    

    if result:
        response = Response(json.dumps(result), status=200,
                            content_type=CONTENT_TYPE_JSON)
    else:
        response = Response("NOT FOUND", status=404,
                            content_type=CONTENT_TYPE_PLAIN_TEXT)
    return response


@app.route("/attendees", methods=["POST"])
def create_attendee():
    return ""


@app.route("/attendees/<uid>", methods=["PUT"])
def update_attendee_by_uid():
    return ""


if __name__ == '__main__':
    app.run(host='localhost', port=5021, debug=False)
