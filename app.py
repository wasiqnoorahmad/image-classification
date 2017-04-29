from flask import (
    Flask,
    request,
    render_template,
    send_from_directory,
    url_for,
    jsonify
)
from PIL import Image
from werkzeug import secure_filename
from classify import image_classify
import os, urllib, requests, imghdr

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

from logging import Formatter, FileHandler
handler = FileHandler(os.path.join(basedir, 'log.txt'), encoding='utf8')
handler.setFormatter(
    Formatter("[%(asctime)s] %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S")
)
app.logger.addHandler(handler)


app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])

def convert_jgp(filename):
    im = Image.open(filename)
    rgb_im = im.convert('RGB')
    out = os.basename(filename) + '.jpp'
    rgb_im.save(out)
    return out


def get_type(filename):
    return imghdr.what(filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'js_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/js', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    elif endpoint == 'css_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/css', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(app.root_path + '/static/css/', filename)


@app.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(app.root_path + '/static/js/', filename)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/classify', methods=['POST', 'GET'])
def classify():
    updir = os.path.join(basedir, 'upload/')
    filename = None
    if request.method == 'POST':
        files = request.files['file']
        if files and allowed_file(files.filename):
            filename = secure_filename(files.filename)
            app.logger.info('FileName: ' + filename)
            files.save(os.path.join(updir, filename))
	    #return jsonify(name=filename, category=category, per=percentage)
    elif request.method == 'GET':
        url = request.args.get('upload')
        filename = str(url).split('/')[-1]
        data = requests.get(url, allow_redirects=True)
        f = open(os.path.join(updir, filename),'wb')
        f.write(data.content)
        f.close()
    if get_type(os.path.join(updir, filename) == 'png'):
	filename = convert_jpg(filename)
    result = image_classify(os.path.join(updir, filename))
    result = result[2:-2]
    percentage = result.split(',')[-1]
    category = ",".join(result.split(',')[:-1]).title()
    #return str('Category: ' + category + '\n' + 'Percentage: ' + percentage)
    return jsonify(name=filename, category=category, per=percentage)


if __name__ == '__main__':
    app.run(debug=True)
