from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback
import numpy as np
import os

from libs import image_helper
from libs.strings import gettext
from libs import ml_model
from schemas.image import ImageSchema

image_schema = ImageSchema()


class ImageUpload(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        """
        This endpoint is used to upload an image file. It uses the
        JWT to retrieve user information and save the image in the user's folder.
        If a file with the same name exists in the user's folder, name conflicts
        will be automatically resolved by appending a underscore and a smallest
        unused integer. (eg. filename.png to filename_1.png).
        """
        plant_dict = {"[0]": "Apple___Apple_scab", 
                    "[1]": "Apple___Black_rot",
                    "[2]": "Apple___Cedar_apple_rust",
                    "[3]": "Apple___healthy",
                    "[4]": "Blueberry___healthy",
                    "[5]": "Cherry_(including_sour)___healthy",
                    "[6]": "Cherry_(including_sour)___Powdery_mildew",
                    "[7]": "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
                    "[8]": "Corn_(maize)___Common_rust_",
                    "[9]": "Corn_(maize)___healthy",
                    "[10]": "Corn_(maize)___Northern_Leaf_Blight", 
                    "[11]": "Grape___Black_rot",
                    "[12]": "Grape___Esca_(Black_Measles)",
                    "[13]": "Grape___healthy",
                    "[14]": "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
                    "[15]": "Orange___Haunglongbing_(Citrus_greening)",
                    "[16]": "Peach___Bacterial_spot",
                    "[17]": "Peach___healthy",
                    "[18]": "Pepper,_bell___Bacterial_spot",
                    "[19]": "Pepper,_bell___healthy",             
                    "[20]": "Potato___Early_blight", 
                    "[21]": "Potato___healthy",
                    "[22]": "Potato___Late_blight",
                    "[23]": "Raspberry___healthy",
                    "[24]": "Soybean___healthy",
                    "[25]": "Squash___Powdery_mildew",
                    "[26]": "Strawberry___healthy",
                    "[27]": "Strawberry___Leaf_scorch",
                    "[28]": "Tomato___Bacterial_spot",
                    "[29]": "Tomato___Early_blight",             
                    "[30]": "Tomato___healthy", 
                    "[31]": "Tomato___Late_blight",
                    "[32]": "Tomato___Leaf_Mold",
                    "[33]": "Tomato___Septoria_leaf_spot",
                    "[34]": "Tomato___Spider_mites Two-spotted_spider_mite",
                    "[35]": "Tomato___Target_Spot",
                    "[36]": "Tomato___Tomato_mosaic_virus",
                    "[37]": "Tomato___Tomato_Yellow_Leaf_Curl_Virus"
        }
        classes = {
            "Apple___Apple_scab": "Apple Scab Disease Detected",
            "Apple___Black_rot": "Apple Black Rot Disease Detected",
            "Apple___Cedar_apple_rust": "Cedar Apple Rust Disease Detected",
            "Apple___healthy":"Healthy Apple Plant",
            "Blueberry___healthy": "Healthy Blueberry Plant",
            "Cherry_(including_sour)___healthy": "Healthy Cherry (Including Sour) Plant",
            "Cherry_(including_sour)___Powdery_mildew": "Powdery Mildew Disease Detected in Cherry (Including Sour)",
            "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": "Cercospora Leaf Spot and Gray leaf Spot Detected in Corn (Maize)",
            "Corn_(maize)___Common_rust_": "Common Rust Detected in Corn (Maize)",
            "Corn_(maize)___healthy": "Healthy Corn (Maize)",
            "Corn_(maize)___Northern_Leaf_Blight": "Northern Leaf Blight Detected in Corn (Maize)",
            "Grape___Black_rot": "Black Rot Disease Detected in Grapes",
            "Grape___Esca_(Black_Measles)": "Esca (Black Measles) Disease Detected in Grape",
            "Grape___healthy": "Healthy Grape Plant",
            "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "Leaf Blight (Isariopsis Leaf Spot) Disease Detected in Grape Plant",
            "Orange___Haunglongbing_(Citrus_greening)": "Haunglongbing (Citrus Greening) Disease Detected in Orange Plant",
            "Peach___Bacterial_spot": "Bacterial Spot Detected in Peach Plant",
            "Peach___healthy": "Healthy Peach Plant",
            "Pepper,_bell___Bacterial_spot": "Bacterial Spot Detected in Pepper Bell Plant",
            "Pepper,_bell___healthy": "Healthy Pepper Bell Plant",
            "Potato___Early_blight": "Early Blight Disease Detected in Potato Plant",
            "Potato___healthy": "Healthy Potato Plant",
            "Potato___Late_blight": "Late Blight Disease Detected in Potato Plant",
            "Raspberry___healthy": "Healthy Raspberry Plant",
            "Soybean___healthy": "Healthy Soybean Plant",
            "Squash___Powdery_mildew": "Powdery Mildew Detected in Squash Plant",
            "Strawberry___healthy": "Healthy Strawberry Plant",
            "Strawberry___Leaf_scorch": "Leaf Scroch Disease Detected in Strawberry Plant",
            "Tomato___Bacterial_spot": "Bacterial Spot Detected in Toamto Plant",
            "Tomato___Early_blight": "Early Blight Disease Detected in Tomato Plant",
            "Tomato___healthy": "Healthy Tomato Plant",
            "Tomato___Late_blight": "Late Blight Disease Detected in Tomato Plant",
            "Tomato___Leaf_Mold": "Leaf Mold Disease Detected in tomato Plant",
            "Tomato___Septoria_leaf_spot": "Septoria Leaf Spot Detected in Tomato Plant",
            "Tomato___Spider_mites Two-spotted_spider_mite": "Spider Mites Disease Detected in Tomato Plant",
            "Tomato___Target_Spot": "Target Spot Detected in Tomato Plant",
            "Tomato___Tomato_mosaic_virus": "Mosaic Virus Detected in Tomato Plant",
            "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "Yellow Leaf Curl Virus Detected in Tomato Plant"
        }
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}/Prediction"
        try:
            # save(self, storage, folder=None, name=None)
            image_helper.save_image(data["image"], folder=folder)
            run = ml_model.MLModel.predict(data["image"])
            index = np.where(run[0] == max(run[0]))
            plant_name = plant_dict["{}".format(index[0])]
            prediction = classes["{}".format(plant_name)]
            # for x in range(1, len(run[0]) + 1):
                # prediction = prediction + " Prediction # " + str(x) + ": " + run[1][x-1] + "?with probabilty " + str(run[0][x-1]) + ","
            # here we only return the basename of the image and hide the internal folder structure from our user
            # basename = image_helper.get_basename(image_path)
            return {"message": "{}".format(prediction)}, 201
        except UploadNotAllowed:  # forbidden file type
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("image_illegal_extension").format(extension)}, 400
    



class Image(Resource):
    @classmethod
    @jwt_required
    def get(cls, filename: str):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}/Prediction"
        if not image_helper.is_filename_safe(filename):
            return {"message": gettext("image_illegal_file_name").format(filename)}, 400
        
        try:
            return send_file(image_helper.get_path(filename, folder=folder))
        except FileNotFoundError:
            return {"message": gettext("image_not_found").format(filename)}, 404 


    @classmethod
    @jwt_required
    def delete(cls, filename: str):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

        if not image_helper.is_filename_safe(filename):
            return {"message": gettext("image_illegal_file_name").format(filename)}, 400
        
        try:
            os.remove(image_helper.get_path(filename, folder=folder))
            return {"message": gettext("image_deleted").format(filename)}
        except FileNotFoundError:
            return {"message": gettext("image_not_found").format(filename)}, 404
        except:
             traceback.print_exc()
             return {"message": gettext("image_deleted_failed")}, 
             


class AvatarUpload(Resource):
    @classmethod
    @jwt_required
    def put(cls):
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        filename = f"user_{user_id}"
        folder = "avatars"
        avatar_path = image_helper.find_image_any_format(filename, folder)
        if avatar_path:
            try:
                os.remove(avatar_path)
            except:
                return {"message": gettext("avatar_delete_failed")}, 500

        try:
            ext = image_helper.get_extension(data["image"].filename)
            new_ext = "jpg"
            avatar = filename + new_ext
            avatar_path = image_helper.save_image(
                data["image"], folder=folder, name=avatar
            )
            basename = image_helper.get_basename(avatar_path)
            return {"message": gettext("avatar_uploaded").format(basename)}, 200
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("image_illegal_extension").format(extension)}, 400


class Avatar(Resource):
    @classmethod
    @jwt_required
    def get(cls, user_id: int):
        folder = "avatars"
        filename = f"user_{user_id}"
        avatar = image_helper.find_image_any_format(filename, folder)
        if avatar:
            return send_file(avatar)
        return {"message": gettext("avatar_not_found")}, 404