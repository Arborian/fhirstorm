import logging
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta

import jwt
from requests_oauthlib import OAuth2Session

log = logging.getLogger(__name__)


def jwt_state(secret, expires_in=300, **claims):
    claims = dict(claims)
    claims.setdefault('exp', datetime.utcnow() + timedelta(seconds=expires_in))
    return jwt.encode(claims, secret)


def jwt_state_validator(secret, **kwargs):
    def validator(state):
        return jwt.decode(state, secret, **kwargs)
    return validator


def authorization_url(
        service, client_id, redirect_uri, scope, state,
        client_secret=None,
        aud=None,
        launch=None):
    conn = service.bind.clone(
        session=OAuth2Session(
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=scope))
    return conn.session.authorization_url(
        service.security.oauth2_uris.authorize,
        client_secret=client_secret,
        aud=aud,
        state=state,
        launch=launch)


def fetch_token(
        service, client_id, redirect_uri,
        code=None,
        authorization_response=None,
        client_secret=None,
        state=None,
        state_validator=None):
    if state_validator:
        pr = urlparse(authorization_response)
        state_validator(parse_qs(pr.query)['state'][0])
    conn = service.bind.clone(
        session=OAuth2Session(
            client_id=client_id,
            redirect_uri=redirect_uri))
    return conn.session.fetch_token(
        token_url=service.security.oauth2_uris.token,
        code=code,
        authorization_response=authorization_response,
        client_id=client_id,
        client_secret=client_secret,
        state=state)
