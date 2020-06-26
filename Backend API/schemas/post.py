from ma import ma
from models.post import PostModel
from models.user import UserModel


class PostSchema(ma.ModelSchema):

    class Meta:
        model = PostModel
        load_only = ("user",)
        dump_only = ("id",)
        include_fk = True