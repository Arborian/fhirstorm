import os
from flask import Flask, request, redirect, jsonify, url_for, abort
from fhirstorm import Connection, auth

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
app = Flask(__name__)
app.config.from_pyfile('../example/auth-tutorial/config-pub.py')


@app.route('/launch')
def launch():
    iss = request.args['iss']
    if iss != app.config['SMART_SERVICE_ROOT']:
        abort(403)
    launch = request.args.get('launch', None)
    conn = Connection(iss)
    service = conn.service()

    state = auth.jwt_state(app.config['JWT_SECRET'])

    authorization_url, state = auth.authorization_url(
        service,
        client_id=app.config['SMART_CLIENT_ID'],
        redirect_uri=url_for('callback', _external=True),
        scope=app.config['SMART_SCOPE'] + ' launch',
        state=state,
        aud=iss,
        launch=launch)
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    global ACCESS_TOKEN
    conn = Connection(app.config['SMART_SERVICE_ROOT'])
    service = conn.service()
    token = auth.fetch_token(
        service,
        client_id=app.config['SMART_CLIENT_ID'],
        redirect_uri=url_for('callback', _external=True),
        authorization_response=request.url,
        state_validator=auth.jwt_state_validator(
            app.config['JWT_SECRET'],
            iss=app.config['SMART_SERVICE_ROOT']))
    print(token)
    ACCESS_TOKEN = token
    return jsonify(token)

