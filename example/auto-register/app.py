import os
import json

import jwt
import requests
from flask import Flask, request, redirect, jsonify, url_for, abort
from fhirstorm import Connection, auth

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
app = Flask(__name__)
app.config.from_pyfile('./config.py')

registrations = {}

@app.route('/register', methods=['POST'])
def register():
    iss = request.json['iss']
    conn = Connection(iss)
    svc = conn.service()
    uris = svc.security.oauth2_uris
    reg_uri = uris.register
    resp = requests.post(
        reg_uri, data=json.dumps(_get_manifest()),
        headers={'Content-Type': 'application/json'})
    print(resp.json())
    resp.raise_for_status()
    registrations[iss] = resp.json()
    return jsonify(resp.json())


@app.route('/launch')
def launch():
    iss = request.args['iss']
    reg = registrations[iss]
    launch = request.args.get('launch', None)
    conn = Connection(iss)
    service = conn.service()

    state = auth.jwt_state(
        app.config['JWT_SECRET'],
        iss=iss)

    print('Found registration', reg)

    authorization_url, state = auth.authorization_url(
        service,
        client_id=reg['client_id'],
        client_secret=reg['client_secret'],
        redirect_uri=url_for('callback', _external=True),
        scope=reg['scope'],
        state=state,
        aud=iss,
        launch=launch)
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    claims = jwt.decode(
        request.args['state'], app.config['JWT_SECRET'])
    iss = claims['iss']
    reg = registrations[iss]
    conn = Connection(iss)
    service = conn.service()
    token = auth.fetch_token(
        service,
        client_id=reg['client_id'],
        client_secret=reg['client_secret'],
        redirect_uri=url_for('callback', _external=True),
        authorization_response=request.url)
    print(token)
    return jsonify(token)


def _get_manifest():
    return {
        "software_id": "com.ehtcares:fhirstorm:1.0",
        "client_name": "FHIRstorm auto-register text",
        "launch_url": url_for('.launch', _external=True),
        "redirect_uris": [
            url_for('.callback', _external=True),
        ],
        "scope": "launch launch/patient openid profile patient/*.read",
        "token_endpoint_auth_method": "client_secret_basic",
        "grant_types": [
            "authorization_code", "refresh_token",
        ],
        "response_types": [
            "code",
        ],
        "fhir_versions": [
            "1.0.2",
            "1.1.0",
            "1.4.0",
            "1.6.0",
            "1.8.0",
            "3.0.1",
        ]
    }
