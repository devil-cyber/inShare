import home, upload_file, download
from __init__ import create_app
import os

# port = int(os.environ.get("PORT"))

app = create_app()


app.add_url_rule("/", view_func=home.home_route)
app.add_url_rule(
    "/api/upload", view_func=upload_file.upload_route, methods=["GET", "POST"]
)
app.add_url_rule("/files/<uuid>", view_func=download.download_route)
app.add_url_rule("/files/download/<filename>", view_func=download.file_download)
app.add_url_rule("/files/send", view_func=download.send_route, methods=["GET", "POST"])
if __name__ == "__main__":
    app.run(debug=True)
