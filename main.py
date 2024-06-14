from flask import Flask
from blueprints import views,encrypt,decrypt,download
import os

app= Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

 

app.secret_key = 'dsnjznodfDSOHIxc;pdsijpknjsrodzfjzsikezds3456789izxoa;djdiOzfcxok;sljknzdv'

app.register_blueprint(views)
app.register_blueprint(encrypt)
app.register_blueprint(decrypt)
app.register_blueprint(download)


if __name__ == "__main__":
    app.run(debug=True)