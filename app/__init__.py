# app/__init__.py
import json
from flask_api import FlaskAPI, status
from flask_sqlalchemy import SQLAlchemy

from flask import request, jsonify, abort, make_response

# local import
from flask_cors import CORS
from instance.config import app_config

# For password hashing
from flask_bcrypt import Bcrypt

# initialize db
db = SQLAlchemy()


def create_app(config_name):

    from app.models import TodoList, User

    app = FlaskAPI(__name__, instance_relative_config=True)
    cors = CORS(app)
    # overriding Werkzeugs built-in password hashing utilities using Bcrypt.
    bcrypt = Bcrypt(app)

    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/todolists/', methods=['POST', 'GET'])
    def todolists():
        # get the access token
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authed
                if request.method == "POST":
                    name = str(request.data.get('name', ''))
                    if name:
                        todolist = TodoList(name=name, created_by=user_id)
                        todolist.save()
                        response = jsonify({
                            'id': todolist.id,
                            'name': todolist.name,
                            'is_completed': todolist.is_completed,
                            'date_created': todolist.date_created,
                            'date_modified': todolist.date_modified,
                            'created_by': user_id
                        })

                        return make_response(response), 201

                else:
                    # GET
                    # get all the todolists for this user
                    todolists = TodoList.get_all(user_id)
                    results = []

                    for todolist in todolists:
                        obj = {
                            'id': todolist.id,
                            'name': todolist.name,
                            'is_completed': todolist.is_completed,
                            'date_created': todolist.date_created,
                            'date_modified': todolist.date_modified,
                            'created_by': todolist.created_by
                        }
                        results.append(obj)

                    return make_response(jsonify(results)), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/todolists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def todolist_manipulation(id, **kwargs):

        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                todolist = TodoList.query.filter_by(id=id).first()
                if not todolist:
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)

                if request.method == "DELETE":
                    todolist.delete()
                    return make_response({}), 204
                elif request.method == 'PUT':
                    if request.data.get('name'):
                        name = str(request.data.get('name'))
                        todolist.name = name
                    is_completed = request.data.get('is_completed', False)
                    todolist.is_completed = is_completed
                    todolist.save()
                    response = {
                        'id': todolist.id,
                        'name': todolist.name,
                        'is_completed': todolist.is_completed,
                        'date_created': todolist.date_created,
                        'date_modified': todolist.date_modified,
                        'created_by': todolist.created_by
                    }
                    return make_response(jsonify(response)), 200
                else:
                    # GET
                    response = jsonify({
                        'id': todolist.id,
                        'name': todolist.name,
                        'is_completed': todolist.is_completed,
                        'date_created': todolist.date_created,
                        'date_modified': todolist.date_modified,
                        'created_by': todolist.created_by
                    })
                    return make_response(response), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
