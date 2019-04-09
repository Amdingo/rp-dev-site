from flask import Blueprint, jsonify, request

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
    username = post.get('username')
    email = post.get('email')
    db.session.add(User(username=username, email=email))
    db.session.commit()
    res = {
        'status': 'success',
        'message': f'user {username} has been created'
    }
    return jsonify(res), 201
