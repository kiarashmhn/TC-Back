import os
from flask import Flask, request, redirect, url_for, Blueprint, session, send_from_directory
from flask.json import jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
from QP import app, ResponseObject, Car, db, auth_manager

UPLOAD_FOLDER = '/Users/kiarash/Desktop/TC-Back/img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
img = Blueprint('img', __name__)


class ImageHandler():
    def __init__(self):
        pass

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def add(self, car, file):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        car.image_url = filename
        db.session.commit()

    def get(self, filename):
        filename = 'img/' + filename
        return send_from_directory(app.static_folder,
                                   filename)


class ImageApiHandler():
    image_handler = ImageHandler()

    def __init__(self):
        pass

    @staticmethod
    @img.route('/<int:car_id>', methods=['POST'])
    @auth_manager.authenticate
    def upload_image(user, car_id):
        """
            This is the UploadCarImage API
            Call this api passing a car_id and a file to add the file as image of the car.
            ---
            tags:
                - UploadCarImage API
            parameters:
                - name: car_id
                  in: path
                  type: integer
                  required: true
                  description: id of the car you want to add image for.
                - name: file
                  in: form
                  type: multipartFile
                  required: true
                  description: the image you want to add for the car.
            responses:
                200:
                    description: Ok
                    schema:
                        type: object
                        properties:
                            status:
                                type: string
                                example: OK

                400,status="Invalid car id!":
                    description: Car not found.
                400,status="No file part!":
                    description: No file parameter in the request.
                400,status="File type not allowed!":
                    description: file type is invalid.
                400,status="No file part!":
                    description: No file parameter in the request.
                400,status="Not allowed!":
                    description: this car isn't yours.
                401:
                    description: You aren't logged in
        """
        image_handler = ImageApiHandler.image_handler
        # check if the post request has the file part
        if 'file' not in request.files:
            out = {'status': 'No file part!'}
            return jsonify(out), 400
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            out = {'status': 'No selected file!'}
            return jsonify(out), 400
        if file and image_handler.allowed_file(file.filename):
            car = Car.query.filter_by(id=car_id).first()
            if car is None:
                out = {'status': 'Invalid car id!'}
                return jsonify(out), 400
            if user.id != car.user_id:
                out = {'status': 'Not allowed!'}
                return jsonify(out), 400
            image_handler.add(car, file)
            out = {'status': 'OK'}
            return jsonify(out), 200
        else:
            out = {'status': 'File type not allowed!'}
            return jsonify(out), 400

    @staticmethod
    @img.route('/<path:filename>', methods=["GET"])
    def download_image(filename):
        """
            This is the DownloadCarImage API
            Call this api passing a filename to download the image.
            ---
            tags:
                - DownloadCarImage API
            parameters:
                - name: filename
                  in: path
                  type: string
                  required: true
                  description: filename of the image.
            responses:
                200:
                    description: OK
                    schema:
                        type: file
                401:
                    description: You aren't logged in
                404:
                    description: file not found
                """
        return ImageApiHandler.image_handler.get(filename)
