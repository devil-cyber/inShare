from __init__ import create_app
from flask import render_template, send_from_directory, request
from db.connect import connect_db
from flask_cors import CORS, cross_origin
from send import send_email
import requests


app = create_app()
client = connect_db()
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "content-type"


def validate(email):
    email_address = email
    response = requests.get(
        "https://isitarealemail.com/api/email/validate", params={"email": email_address}
    )
    status = response.json()["status"]
    if status == "valid":
        return "valid"
    elif status == "invalid":
        return "invalid"
    else:
        return "unknown"


@app.route("/files/send", methods=["GET", "POST"])
@cross_origin()
def send_route():
    if request.method == "POST":
        data_js = request.json
        uuid = data_js["uuid"]
        emailTo = data_js["emailTo"]
        emailFrom = data_js["emailFrom"]
        if validate(emailTo) == "invalid" or validate(emailTo) == "unknown":
            return {"success": "reciverinvalid"}
        elif validate(emailFrom) == "invalid" or validate(emailFrom) == "unknown":
            return {"success": "senderinvalid"}
        else:

            db = client.file
            db = db["file_upload"]
            data = db.find_one({"uuid": uuid})
            sender = emailFrom
            reciver = emailTo
            size = str(data["size"]) + "KB"
            expires = "Expires in 24 hours"
            download_link = f"https://fileinshare.herokuapp.com/files/{uuid}"
            send_email(sender, size, expires, download_link, reciver)

            return {"success": "Email sent successfully"}


@app.route("/files/<uuid>", methods=["GET"])
def download_route(uuid):
    db = client.file
    db = db["file_upload"]
    data = db.find_one({"uuid": uuid})

    if data != None:
        print(data)
        filename = data["filename"]
        path = data["path"]
        download_path = f"/files/download/{filename}"
        size = data["size"]
        print(filename, path, size)
        return render_template(
            "download.html", filename=filename, size=size, path=download_path
        )
    else:
        e = "Given Link not Found on server Sorry:)"
        return render_template("404.html", e=e)


@app.route("/files/download/<filename>")
def file_download(filename):
    try:
        d = send_from_directory("uploads", filename, as_attachment=True)
        return d
    except Exception as e:
        print(str(e))
