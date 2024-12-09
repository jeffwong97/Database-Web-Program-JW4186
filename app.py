from flask import Flask

UPLOAD_FOLDER = 'ProductPhotos'

app = Flask(__name__)
app.secret_key = "afdhuaisfo3w8efaof9428e9afuaf"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
