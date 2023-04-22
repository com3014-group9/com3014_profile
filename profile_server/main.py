from flask import Flask, Blueprint, current_app, g, request
from auth_middleware import auth_required
from pymongo import MongoClient

profiler = Blueprint('profiler', __name__, url_prefix='/profile')

def create_app():
    app = Flask(__name__)
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
    user = get_db().profile_data.find_one({"user_id": user_id})
    if user is not None:
        get_db().profile_data.insert_one({
            'user_id': user_id,
            'user_name' : f"user_{user_id}", 
            'pfp' : None, 
            'follows' : [],
            'followed_by' : []
        })

        return 200
    else:
        return 404 

@profiler.route('/update_user_pfp', methods=['POST'])
@auth_required
def update_user_pfp(user_id):
    user = get_db().profile_data.find_one({"user_id": user_id})
    if user is not None and "pfp" in request.form:
        query = { "user_id": user_id }
        values = { "$set": { "pfp": request.form['pfp'] } }
        get_db().profile_data.update_one(query, values)

        return 200 
    elif user is not None:
        return 400
    else:
        return 404 

@profiler.route('/get_followers', methods=['GET'])
def get_followers():
    if "user_id" not in request.form:
        return 400 
    
    user = get_db().profile_data.find_one({"user_id": request.form["user_id"]})
    if user is not None:
        return user["followed_by"], 200
    return 404
    
@profiler.route('/get_follows', methods=['GET'])
def get_follows():
    if "user_id" not in request.form:
        return 400 
    
    user = get_db().profile_data.find_one({"user_id": request.form["user_id"]})
    if user is not None:
        return user["follows"], 200
    return 404 

@profiler.route('/follow_user', methods=['POST'])
@auth_required
def follow_user(user_id):
    if "user_to_follow" not in request.form:
        return 400 

    user = get_db().profile_data.find_one({"user_id": request.form["user_id"]})
    if user is not None:
        query = { "user_id": user_id }
        values = {'$push': {'follows': request.form["user_to_follow"]}}
        get_db().profile_data.update_one(query, values)

        query = { "user_id": request.form["user_to_follow"] }
        values = {'$push': {'followed_by': user_id}}
        get_db().profile_data.update_one(query, values)

        return 200 
    elif user is not None:
        return 400
    else:
        return 404 

@profiler.route('/unfollow_user', methods=['POST'])
@auth_required
def unfollow_user(user_id):
    if "user_to_unfollow" not in request.form:
        return 400 

    user = get_db().profile_data.find_one({"user_id": request.form["user_id"]})
    if user is not None:
        query = { "user_id": user_id }
        values = {'$pull': {'follows': request.form["user_to_unfollow"]}}
        get_db().profile_data.update_one(query, values)

        query = { "user_id": request.form["user_to_unfollow"] }
        values = {'$pull': {'followed_by': user_id}}
        get_db().profile_data.update_one(query, values)

        return 200 
    elif user is not None:
        return 400
    else:
        return 404 

if __name__ == "__main__":
    profile_db = get_db_client().com3014_profiles
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5051)