from flask import Flask, Blueprint, current_app, g, request
from auth_middleware import auth_required
from pymongo import MongoClient
from flask_cors import CORS

profiler = Blueprint('profiler', __name__, url_prefix='/profile')

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(profiler)

    app.teardown_appcontext_funcs.append(close_db)

    return app

def get_db_client():
    client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")

    return client

def get_db():
    if 'db' not in g:
        g.db = get_db_client()
    
    return g.db.com3014_profiles

def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@profiler.route('/create_user', methods=['POST'])
@auth_required
def create_user(user_id):
    username = request.get_json().get('username')
    user = get_db().profile_data.find_one({"user_id": user_id})
    if user is None:
        get_db().profile_data.insert_one({
            'user_id': user_id,
            'user_name' : username, 
            'pfp' : None, 
            'follows' : [],
            'followed_by' : []
        })

        return {"user_id": user_id}, 200
    else:
        return {"error": "User already exists"}, 400
    
@profiler.route('/get_user_info', methods=['GET'])
def get_user_info():
    user_id = request.args.get("user_id")
    if user_id is None:
        return {"error": "Bad request, user_id missing"}, 400

    user = get_db().profile_data.find_one({"user_id": request.args.get("user_id")})
    if user is not None:
        return {
            "user_id": user["user_id"],
            "user_name": user["user_name"],
            "pfp": user["pfp"],
            "followers": user["followed_by"],
            "follows": user["follows"]
        }, 200
    else:
        return {"error": "User not found"}, 404
    
@profiler.route('/update_user_pfp', methods=['POST'])
@auth_required
def update_user_pfp(user_id):
    user = get_db().profile_data.find_one({"user_id": user_id})
    if user is not None and 'pfp' in request.files:
        query = { "user_id": user_id }
        values = { "$set": { "pfp": request.files['pfp'] } }
        get_db().profile_data.update_one(query, values)

        return {"pfp" : request.files['pfp']}, 200 
    elif user is None:
        return {"error": "User doesn't exist"}, 404
    else:
        return {"error": "MEOW I'M A CAT"}, 404 

@profiler.route('/get_followers', methods=['GET'])
def get_followers():
    user_id = request.args.get("user_id")
    if user_id is None:
        return {"error" : "Bad request, try again"},
    
    user = get_db().profile_data.find_one({"user_id": request.args.get("user_id")})
    if user is not None:
        return {"followers": user["followed_by"]}, 200
    return {"error" : "User not found"}, 404
    
@profiler.route('/get_follows', methods=['GET'])
def get_follows():
    user_id = request.args.get("user_id")
    if user_id is None:
        return {"error" : "Bad request, try again"}, 400 
    
    user = get_db().profile_data.find_one({"user_id": request.args.get("user_id")})
    if user is not None:
        return {"follows": user["follows"]}, 200
    return {"error" : "User not found"}, 404 

@profiler.route('/follow_user', methods=['POST'])
@auth_required
def follow_user(user_id):
    if "user_to_follow" not in request.get_json():
        return {"error" : "Bad request, try again"}, 400

    if get_db().profile_data.find_one({"user_id": request.get_json().get('user_to_follow')}) == None:
        return {"error" : "Unable to follow user that doesn't exist"}, 404

    user = get_db().profile_data.find_one({"user_id": user_id})
    if user is not None:
        query = { "user_id": user_id }
        values = {'$push': {'follows': request.get_json().get('user_to_follow')}}
        get_db().profile_data.update_one(query, values)
        query = { "user_id": request.get_json().get("user_to_follow") }
        values = {'$push': {'followed_by': user_id}}
        get_db().profile_data.update_one(query, values)

        return {"user_to_follow" : request.get_json().get('user_to_follow')}, 200 
    elif user is None:
        return {"error" : "User not found"}, 404
    else:
        return {"error" : "Something went wrong, try again"}, 400 

@profiler.route('/unfollow_user', methods=['POST'])
@auth_required
def unfollow_user(user_id):
    if "user_to_unfollow" not in request.get_json():
        return {"error" : "Bad request, try again"}, 400 

    if get_db().profile_data.find_one({"user_id": request.get_json().get('user_to_unfollow')}) == None:
        return {"error" : "Unable to follow user that doesn't exist"}, 404

    user = get_db().profile_data.find_one({"user_id": user_id})
    if user is not None:
        query = { "user_id": user_id }
        values = {'$pull': {'follows': request.get_json().get('user_to_unfollow')}}
        get_db().profile_data.update_one(query, values)

        query = { "user_id": request.get_json().get('user_to_unfollow') }
        values = {'$pull': {'followed_by': user_id}}
        get_db().profile_data.update_one(query, values)

        return {"user_to_unfollow" : request.get_json().get('user_to_unfollow')}, 200 
    elif user is None:
        return {"error" : "User not found"}, 400
    else:
        return {"error" : "Something went wrong, try again"}, 404 

if __name__ == "__main__":
    profile_db = get_db_client().com3014_profiles
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5051)