from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.api.models import User
from project import db


users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/users/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'success',
        'message': 'healthy'
    })


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post = request.get_json()
    res = {
        'status': 'fail',
        'message': 'Invalid payload'
    }
    if not post:
        return jsonify(res), 400
    username = post.get('username')
    email = post.get('email')
    try:
        u = User.query.filter_by(email=email).first()
        if not u:
            db.session.add(User(username=username, email=email))
            db.session.commit()
            res['status'] = 'success'
            res['message'] = f'user {username} has been created'
            return jsonify(res), 201
        else:
            res['message'] = 'Sorry, that email address is already in use.'
            return jsonify(res), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(res), 400


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user details"""
    res = {
        'status': 'fail',
        'message': 'User does not exist'
    }
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(res), 404
        else:
            res = {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'active': user.active
                }
            }
            return jsonify(res), 200
    except ValueError:
        return jsonify(res), 404


@users_blueprint.route('/users', methods=['GET'])
def get_users():
    """Gets the users"""
    res = {
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
        }
    }
    return jsonify(res), 200
