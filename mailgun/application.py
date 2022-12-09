from flask import Flask, Response, request
from datetime import datetime
from flask_cors import CORS
import json

application = app = Flask(__name__)
CORS(app)


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


@app.route("/api/students/<uni>", methods=["GET"])
def get_student_by_uni(uni):

    result = ColumbiaStudentResource.get_by_key(uni)

    if result:
        rsp = Response(json.dumps(result), status=200,
                       content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011, debug=True)
