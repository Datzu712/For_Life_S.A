from flask import jsonify, session, g, redirect, request, url_for
from functools import wraps
from os import environ
import jwt
from werkzeug.exceptions import Forbidden

from ..extensions import db, redis_client
from ..database.models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get('access_token')
        if not token:
            if request.method == 'GET':
                return redirect(url_for('app.auth.login'))
            else:
                raise Forbidden()

        try:
            data = jwt.decode(token, environ.get('SECRET_KEY'), algorithms=['HS256'])
            current_user = db.session.query(User).filter_by(id=data['userId']).first()

            if not current_user:
                return jsonify({ 'message': 'Forbidden' }), 403
            
            cached_session = redis_client.get(f'sessions:{current_user.id}').decode('utf-8')
            if not cached_session or cached_session != token:
                raise Forbidden()
            
            g.current_user = current_user
            redis_client.setex(f'sessions:{current_user.id}', 1800, token) # reset token ttl
        except Exception as e:
            print(e)
            if request.method == 'GET':
                return redirect(url_for('app.auth.login'))
            else:
                raise Forbidden()

        return f(*args, **kwargs)
    return decorated