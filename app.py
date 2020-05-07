import os
import re

from flask import Flask, abort, request

GUID_RE = re.compile(
    r"\A[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\Z"
)
UPLOAD_DIRECTORY = "/var/uploads/"

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 512


@app.route("/", methods=["GET"])
def root():
    return "", 204


@app.route("/files/", methods=["POST"])
def add_file():
    if request.headers.get("Content-Type") != "text/plain":
        abort(422)

    guid = request.headers.get("X-guid", "")
    if not GUID_RE.match(guid):
        abort(422)

    with open(os.path.join(UPLOAD_DIRECTORY, guid), "wb") as fp:
        fp.write(request.data)
    return "", 201


@app.route("/files/<guid>", methods=["GET"])
def get_file(guid):
    if not GUID_RE.match(guid):
        abort(422)

    filepath = os.path.join(UPLOAD_DIRECTORY, guid)
    if not os.path.isfile(filepath):
        abort(404)

    with open(filepath) as fp:
        return fp.read(), {"Content-Type": "text/plain"}
