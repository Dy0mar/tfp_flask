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


@app.route('/api/users/', methods=['GET'])
@requires_auth
def get_users():
    items = User.query.all()
    return jsonify(users=[item.serialize for item in items], error=False)


@app.route('/api/delete/<int:user_id>', methods=['DELETE'])
@requires_auth
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        raise CommonError(
            {"code": "user_no_found", "description": "User not found"}, 401
        )
    ctx = _request_ctx_stack.top

    data = {'delete': 'ok'}
    if user.email == ctx.current_user.get('email'):
        data['logout'] = True
        db.session.delete(user)
        db.session.commit()

    return jsonify(**data)


@app.route('/api/get-access/', methods=['POST'])
def get_access():
    if request.method == 'POST':
        email = request.json.get('email')
        assert email
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify(error=True, message="email is already exists")

        token = secrets.token_urlsafe(64)
        user = User(email=email, token=token, access=True)

        # save to db
        db.session.add(user)
        db.session.commit()

        base_url = app.config.get('BASE_URL')
        # send mail
        user.send_email_for_confirmation(base_url)
        return jsonify(create='ok', error=False)

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
    user.hit += 1
    db.session.add(user)
    db.session.commit()

    jwt_token = jwt.encode(
        {'email': user.email}, app.config.get('SECRET_KEY'), algorithm='HS256')
    return jsonify(token=jwt_token.decode())
