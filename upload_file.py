from __init__ import create_app
from flask import render_template, request, flash
from werkzeug.utils import secure_filename
import uuid
import os
from db.connect import connect_db, add_file
from flask_cors import CORS, cross_origin

app = create_app()
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "content-type"
app.config["MAX_CONTENT_LENGTH"] = app.config["MAX_CONTENT_LENGTH"]

client = connect_db()


@app.route("/api/upload", methods=["POST", "GET"])
@cross_origin()
def upload_route():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return {"message": "Upload the file !!"}
        file = request.files["file"]

        filename = secure_filename(file.filename)
        try:

            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            size = os.stat(os.path.join(app.config["UPLOAD_FOLDER"], filename)).st_size
            uuid_data = uuid.uuid4().hex
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            add_file(client, filename, uuid_data, path, size)
            return {
                "file": f"{app.config['BASE_URL']}/files/{uuid_data}",
                "status": 200,
            }

        except Exception as e:
            return {"file": f"{str(e)}", "status": 200}
