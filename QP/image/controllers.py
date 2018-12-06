import os
from flask import Flask, request, redirect, url_for, Blueprint, session, send_from_directory
from flask.json import jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
from QP import app, ResponseObject, Car, db

UPLOAD_FOLDER = '/Users/kiarash/Desktop/TC-Back/img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
img = Blueprint('img', __name__)


class ImageHandler:
    def __init__(self):
        pass

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    @staticmethod
    @login_required
    @img.route('/<int:car_id>', methods=['POST'])
    def upload_image(car_id):
        # check if the post request has the file part
        if 'file' not in request.files:
            response = ResponseObject.ResponseObject(obj=None, status='No file part!')
            return jsonify(response.serialize())
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            response = ResponseObject.ResponseObject(obj=None, status='No selected file!')
            return jsonify(response.serialize())
        if file and ImageHandler.allowed_file(file.filename):
            car = Car.query.filter_by(id=car_id).first()
            if car is None:
                response = ResponseObject.ResponseObject(obj=None, status='Invalid car id!')
                return jsonify(response.serialize())
            if session['user_id'] != car.user_id:
                response = ResponseObject.ResponseObject(obj=None, status='You are not allowed to /'
                                                                          'upload image for this car!')
                return jsonify(response.serialize())
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            car.image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            db.session.commit()
            response = ResponseObject.ResponseObject(obj=None, status='OK')
            return jsonify(response.serialize())
        else:
            response = ResponseObject.ResponseObject(obj=None, status='File type not allowed!')
            return jsonify(response.serialize())

    @staticmethod
    @img.route('/<path:filename>', methods=["GET"])
    def download_image(filename):
        filename = 'img/' + filename
        return send_from_directory(app.static_folder,
                                   filename)
