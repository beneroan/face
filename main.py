import os
from flask import jsonify
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import uuid
from identify_face import identify

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/identify', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'GET':
      return '''
         <!doctype html>
         <title>Upload new File</title>
         <h1>Upload new File</h1>
         <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
         </form>
         '''

   if 'file' not in request.files:
      return 'err 1'
   
   file = request.files['file']

   if file and file.filename != '' and allowed_file(file.filename):
      filename = str(uuid.uuid1()) + secure_filename(file.filename)
      print((os.path.join(app.config['UPLOAD_FOLDER'], filename)))
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

      identity = identify(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      print(identity)
      
      return jsonify({ 'id': identity.person_id, 'confidence': identity.confidence })
      
   return 'err 2'

# if __name__ == '__main__':
#    app.run(port=6000)
