import os
import secrets
from functools import wraps

import jwt
from flask import Flask, request, jsonify, _request_ctx_stack
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from app.config import DevelopmentConfig, ProductionConfig

key = 'secret_key'


def get_config():
    if os.environ.get('FLASK_ENV') == 'production':
        return ProductionConfig
    if os.environ.get('FLASK_ENV') == 'development':
        return DevelopmentConfig


app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)
app.config.from_object(get_config())

db = SQLAlchemy(app)

mail = Mail(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


from .models import User


class BaseError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.error['error'] = True
        self.status_code = status_code


class AuthError(BaseError):
    pass


class CommonError(BaseError):
    pass


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@app.errorhandler(CommonError)
def handle_common_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header"""

    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return app.send_static_file('index.html')


def requires_auth(f):
    """Determines if the Access Token is valid"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        try:
            payload = jwt.decode(
                token, app.config.get('SECRET_KEY'), algorithms='HS256'
            )
        except Exception:
            raise AuthError({
                "code": "invalid_header",
                "description": "wrong authentication data."
            }, 401)

        _request_ctx_stack.top.current_user = payload
        return f(*args, **kwargs)
    return decorated


def get_current_user():
    current_user_email = _request_ctx_stack.top.current_user.get('email')
    user = User.query.filter_by(email=current_user_email).first()
    return user


@app.route('/api/users/', methods=['GET'])
@requires_auth
def get_users():
    user = get_current_user()
    if not user.access:
        return jsonify(access=False)

    items = User.query.all()
    data = {
        'access': True,
        'is_admin': user.is_admin,
        'users': [item.serialize for item in items],
        'current_user_email': user.email
    }
    return jsonify(**data)


@app.route('/api/delete/<int:user_id>', methods=['DELETE'])
@requires_auth
def delete_user(user_id):
    current_user = get_current_user()
    deletion_obj = User.query.filter_by(id=user_id).first()

    if not deletion_obj:
        raise CommonError(
            {"code": "user_no_found", "description": "User not found"}, 401
        )

    data = {}
    if deletion_obj.email == current_user.email:
        data['logout'] = True
        db.session.delete(deletion_obj)
        db.session.commit()

    elif current_user.is_admin:
        db.session.delete(deletion_obj)
        db.session.commit()

    return jsonify(**data)


@app.route('/api/set-access/<int:user_id>', methods=['GET'])
@requires_auth
def set_access(user_id):
    current_user = get_current_user()

    data = {}
    if current_user.is_admin:
        user = User.query.filter_by(id=user_id).first()
        user.access = False if user.access else True
        db.session.add(user)
        db.session.commit()
        data = {**user.serialize}

        return jsonify(**data)
    return jsonify(**data)


@app.route('/api/get-access/', methods=['POST'])
def get_access():
    if request.method == 'POST':
        data = {
            'create': 'ok',
            'error': False
        }
        email = request.json.get('email')
        assert email
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify(error=True, message="email is already exists")

        token = secrets.token_urlsafe(64)
        user = User(email=email, token=token)

        base_url = app.config.get('BASE_URL')
        # send mail
        send = user.send_email_for_confirmation(base_url)

        # save to db
        if send:
            db.session.add(user)
            db.session.commit()
        else:
            data = {
                'error': True,
                'message': 'Email sending failed'
            }

        return jsonify(**data)

    return jsonify(error=True)


@app.route('/api/confirm/')
def confirm():
    token = request.args.get('token')

    user = User.query.filter_by(token=token).first()
    if not user:
        raise CommonError(
            {"code": "user_no_found", "description": "User not found"}, 404
        )

    if not user.email_confirmed:
        user.email_confirmed = True
        user.access = True
    user.hit += 1
    db.session.add(user)
    db.session.commit()

    jwt_token = jwt.encode(
        {'email': user.email}, app.config.get('SECRET_KEY'), algorithm='HS256')
    return jsonify(token=jwt_token.decode())
