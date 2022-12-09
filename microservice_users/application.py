from flask import Flask, Response, request
from datetime import datetime
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from nimbus_users import Nimbus_Users
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


@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "Users_Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    response = Response(json.dumps(msg), status=200,
                        content_type=CONTENT_TYPE_JSON)
    return response


@app.route("/users/<uid>", methods=["GET"])
def get_user_by_uid(uid):
    result = Nimbus_Users.get_by_uid(uid)
    

    if result:
        response = Response(json.dumps(result), status=200,
                            content_type=CONTENT_TYPE_JSON)
    else:
        response = Response("NOT FOUND", status=404,
                            content_type=CONTENT_TYPE_PLAIN_TEXT)
    return response


@app.route("/users/<uid>/address", methods=["GET"])
def get_user_address(uid):
    return ""


@app.route("/users", methods=["POST"])
def create_user():
    return ""


@app.route("/users/<uid>/address", methods=["POST"])
def create_user_address():
    return ""


@app.route("/users/<uid>", methods=["PUT"])
def update_user_by_uid():
    return ""


@app.route("/users/<uid>/address", methods=["PUT"])
def update_user_address():
    return ""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)
