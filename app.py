import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, send_from_directory, jsonify, request

# Initialize the Flask application
from numpy.core.tests.test_numerictypes import read_values_nested

app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg', 'png'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/classify', methods=['POST'])
def classify():
    file = request.files['file']
    print(file)
    return jsonify({'mess' : 'Sheikh'})


    # # Get the name of the uploaded file
    # file = request.files['file']
    # print(file)
    # # Check if the file is one of the allowed types/extensions
    # if file and allowed_file(file.filename):
    #     # Make the filename safe, remove unsupported chars
    #     filename = secure_filename(file.filename)
    #     # Move the file form the temporal folder to
    #     # the upload folder we setup
    #     basedir = os.path.abspath(os.path.dirname(__file__))
    #     file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
    #     return jsonify({'mess' : 'Wasiq'})
        #return 	classify('uploads/' + filename)

        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
#        return "Hello"#redirect(url_for('uploaded_file',filename=filename))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=int("88"),
        debug=True
    )
