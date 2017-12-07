import os

from flask import Flask, request, redirect, jsonify
from flask_cors import CORS

from fhirstorm import Connection, auth

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
app = Flask(__name__)

JWT_SECRET = 'itsaseekrit'
REDIRECT_URI = 'http://localhost:5000/redirect'
REDIRECT_URI2 = 'http://localhost:5000/redirect2'
SERVICE_ROOT = 'https://sb-fhir-dstu2.smarthealthit.org/smartdstu2/data'
CLIENT_ID = '9644d85e-07f0-4962-a78b-ab1bfe39c6d8'
CLIENT_SECRET = None
# CLIENT_SECRET = 'L4YpIzPyt48Ih7TTl7stWxWz0eQM3I-TU2QCjs_iL5ZdLNrSFy7fNUCCEL48nB3enl6GASy8v86oMBnMtfxIAA'
SCOPE = 'launch patient/*.* openid profile offline_access'
SCOPE += ' launch/patient'


@app.route('/redirect')
def callback():
    print(request.url)
    return f'The callback URL is {request.url}'


@app.route('/redirect2')
def callback2():
    conn = Connection(SERVICE_ROOT)
    md = conn.metadata
    service = md.rest[0]
    token = auth.fetch_token(
        service,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI2,
        authorization_response=request.url,
        state_validator=auth.jwt_state_validator(JWT_SECRET))
    return jsonify(token)


@app.route('/launch')
def launch():
    iss = request.args['iss']
    launch = request.args.get('launch', None)
    conn = Connection(iss)
    md = conn.metadata
    service = md.rest[0]

    state = auth.jwt_state(JWT_SECRET)

    authorization_url, state = auth.authorization_url(
        service,
        client_id=CLIENT_ID,
        redirect_uri=REDIRECT_URI2,
        scope=SCOPE,
        state=state,
        launch=launch)
    print(authorization_url)

    return redirect(authorization_url)


