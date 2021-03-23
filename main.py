from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# CONFIG
app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usersDB.db"
db = SQLAlchemy(app)


# USER MODEL
class userModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)

    def __repr(self):
        return "User(name = {}, age = {})".format(name, age)


# Args Parser
user_put_args = reqparse.RequestParser()
user_put_args.add_argument("name", type=str, help="name of User", required=True)
user_put_args.add_argument("age", type=int, help="age of User", required=True)

user_patch_args = reqparse.RequestParser()
user_patch_args.add_argument("name", type=str, help="name of User")
user_patch_args.add_argument("age", type=int, help="age of User")

# Output Serializer
userDBObject = {"id": fields.Integer, "name": fields.String, "age": fields.Integer}


# Endpoints
class UserDetails(Resource):
    @marshal_with(userDBObject)
    def get(self, userID):
        result = userModel.query.filter_by(id=userID).first()
        if not result:
            abort(404, message="No such user in DB")
        return result, 201

    @marshal_with(userDBObject)
    def put(self, userID):
        result = userModel.query.filter_by(id=userID).first()
        if result:
            abort(409, message="User with same ID already Exists")

        args = user_put_args.parse_args()
        user = userModel(id=userID, name=args["name"], age=args["age"])
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(userDBObject)
    def patch(self, userID):
        result = userModel.query.filter_by(id=userID).first()
        if not result:
            abort(404, message="No such user in DB")

        args = user_patch_args.parse_args()
        if args["name"]:
            result.name = args["name"]
        if args["age"]:
            result.age = args["age"]

        db.session.commit()

        return result

    def delete(self, userID):
        result = userModel.query.filter_by(id=userID).first()
        if not result:
            abort(404, message="No such user in DB")

        db.session.delete(result)
        db.session.commit()
        return {"message": "Delete Succesful"}, 201


api.add_resource(UserDetails, "/user/<int:userID>")

if __name__ == "__main__":
    app.run(debug=True)
