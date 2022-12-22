from flask import Flask, Response, request, render_template, redirect
from datetime import datetime, date
import json
from columbia_student_resource import ColumbiaStudentResource
from nimbus_resource import NimbusResource
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

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


@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "F22-Starter-Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200,
                      content_type="application/json")

    return result


# Event API
@app.route("/event", methods=["GET"])
def all_events():
    result = NimbusResource.get_events()

    if result:
        rsp = Response(json.dumps(result, default=str), status=200,
                       content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@app.route("/event/<event_id>", methods=["GET", "DELETE", "PUT"])
def event(event_id):
    # handle different requests for this uri
    if request.method == "GET":
        result = NimbusResource.get_event_info(event_id)
    elif request.method == "PUT":
        result = NimbusResource.update_event(request.form)
    else:
        result = NimbusResource.delete_event(event_id)

    if result:
        rsp = Response(json.dumps(result, default=str), status=200,
                       content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


@app.route("/event/<event_id>/attendees", methods=["GET"])
def get_attendees(event_id):
    result = NimbusResource.get_event_attendees(event_id)
    if result:
        rsp = Response(json.dumps(result, default=str), status=200,
                       content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


@app.route("/event/attendee/<attendee_id>", methods=["GET"])
def get_users_events(attendee_id):
    result = NimbusResource.get_users_events(attendee_id)
    if result:
        rsp = Response(json.dumps(result, default=str), status=200,
                       content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


@app.route("/event/organizer/<organizer_id>", methods=["GET"])
def get_organizers_events(organizer_id):
    result = NimbusResource.get_organizer_events(organizer_id)
    if result:
        rsp = Response(json.dumps(result, default=str), status=200,
                       content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@app.route("/event/create", methods=["POST"])
def create_event():
    req_body = request.get_json(force=True)
    result = NimbusResource.create_event(req_body.get(
        'event_info', None), req_body.get('loc_info', None))
    if result:
        rsp = Response(json.dumps(result, default=str), status=200,
                       content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


@app.route("/event/<event_id>/register", methods=["POST"])
def event_registration(event_id):
    req = request.get_json(force=True)
    attendee_id = req.get('attendee_id', None)

    result = NimbusResource.register_for_event(attendee_id, event_id)
    if result:
        rsp = Response(json.dumps(result, default=str), status=200,
                       content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


@app.route("/event/<event_id>/unregister", methods=["DELETE"])
def event_unregistration(event_id):
    print(request.get_json())
    attendee_id = request.get_json()['attendee_id']

    result = NimbusResource.unregister_for_event(attendee_id, event_id)
    if result:
        rsp = Response(json.dumps(result, default=str), status=200,
                       content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011, debug=True)
