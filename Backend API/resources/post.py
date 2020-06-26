import traceback
from uuid import uuid4
import os
from datetime import datetime

from flask_restful import Resource
from flask import request
from flask_uploads import UploadNotAllowed
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims

from models.post import PostModel
from models.user import UserModel
from schemas.post import PostSchema
from schemas.image import ImageSchema
from libs import image_helper
from libs.strings import gettext

post_schema = PostSchema()
image_schema = ImageSchema()
post_schema_list = PostSchema(many=True)


class PostUpload(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        unique = uuid4().hex
        post_json = request.get_json()
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        post_json["user_id"] = user_id
        post_json["username"] = user.username

        post_image = unique + "." + post_json["post_image"]
        post_json["post_image"] = f"/static/images/user_{user_id}/Post/{post_image}"

        post = post_schema.load(post_json)
        try:
            post.save_to_db()
            f = open("imagename.txt", "w+")
            f.write(unique)
            f.close()
            return {"message": "Post Added Successfully"}, 201
        except:
            traceback.print_exc()
            return {"message": "Some error occur"}, 500



class PostImageUpload(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}/Post"
        f = open("imagename.txt", "r")
        content = f.read()
        ext = image_helper.get_extension(data["image"].filename)
        Image = content + ext
        try:
            # save(self, storage, folder=None, name=None)
            image_helper.save_image(data["image"], folder=folder, name=Image)
            print(Image)
            f.close()
            d = open("imagename.txt", "w+")
            d.write("")
            d.close()
            
            # here we only return the basename of the image and hide the internal folder structure from our user
            return {"message": "post image uplaod successfully."}, 201
        except UploadNotAllowed:  # forbidden file type
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("image_illegal_extension").format(extension)}, 400


class Post(Resource):
    @classmethod
    @jwt_required
    def get(cls, post_id: int):
        post = PostModel.find_by_id(post_id)
        if not post:
            return {"message": "Post not found."}
        return post_schema.dump(post), 200

    @classmethod
    @jwt_required
    def delete(cls, post_id: int):
        post = PostModel.find_by_id(post_id)
        if post:
            post.delete_from_db()
            return {"message": "Deleted Successfully."}
        return {"message": "Post not found."}


class PostListOfUser(Resource):
    @classmethod
    @jwt_required
    def get(cls, user_id: int):
        return {"posts": post_schema_list.dump(PostModel.find_by_user_id(user_id))}


class PostList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return {"posts": post_schema_list.dump(PostModel.find_all())}