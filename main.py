from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

# CONFIG
app = Flask(__name__)
api = Api(app)

db = {}
# Args Parser
user_put_args = reqparse.RequestParser()
user_put_args.add_argument("name", type=str, help="name of User", required=True)
user_put_args.add_argument("age", type=int, help="age of User", required=True)

user_patch_args = reqparse.RequestParser()
user_patch_args.add_argument("name", type=str, help="name of User")
user_patch_args.add_argument("age", type=int, help="age of User")


# Endpoints
class UserDetails(Resource):
    def get(self, userID):
        if userID not in db:
            abort(404, message="No such user in DB")

        return {"data": db[userID]}

    def put(self, userID):
        if userID in db:
            abort(409, message="User with same ID already Exists")

        args = user_put_args.parse_args()
        db[userID] = args
        return {"data": db[userID]}, 201

    def patch(self, userID):
        if userID not in db:
            abort(404, message="No such user in DB")

        args = user_patch_args.parse_args()
        if args["name"]:
            db[userID].name = args["name"]
        if args["age"]:
            db[userID].age = args["age"]

        return db[userID], 201

    def delete(self, userID):
        if userID not in db:
            abort(404, message="No such user in DB")

        del db[userID]
        return {"message": "Delete Succesful"}, 201


api.add_resource(UserDetails, "/user/<int:userID>")

if __name__ == '__main__':
    app.run(debug=True)
