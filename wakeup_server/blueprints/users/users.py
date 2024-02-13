from flask import Blueprint, request, jsonify
from models.users import User
from sqlalchemy.exc import IntegrityError
from wakeup_server.fhir_retrive.patient_to_fetch import nameFetch

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/users', methods=['POST'])
def create_user():
  data = request.get_json()
  
  gosh_id = data.get('gosh_id')

  if gosh_id is None:
    return "No GOSH ID provided", 400
  
  try:
    first_name, last_name= nameFetch(gosh_id)

    user = User(first_name, last_name, gosh_id)
    user.create()
    return user.json(), 200
      
  except IntegrityError as e:
      if "UNIQUE constraint failed: users.gosh_id" in str(e):
          return "A user with this GOSH ID already exists", 400
      return "User already exists", 400
  except Exception as e:
      print(e)
      return "Unknown error", 400
    

@users_blueprint.route('/users', methods=['GET'])
def get_users():
  users = User.find_all()
  return jsonify([user.json() for user in users]), 200


@users_blueprint.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
  user = User.find_by_id(user_id)
  if user:
    return jsonify(user.json()), 200
  return "User not found", 404


@users_blueprint.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
  if User.delete_by_id(user_id):
    return "User deleted successfully", 200
  return "User not found", 404


@users_blueprint.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
  data = request.get_json()
  if User.update_by_id(user_id, data):
    return "User updated successfully", 200
  return "Could not update user", 400
