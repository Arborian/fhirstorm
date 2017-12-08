import os

from flask import Flask, request, redirect, jsonify, url_for

from fhirstorm import Connection, auth

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
app = Flask(__name__)

CLIENTS = {
    'confidential': {
        'client_id': '9644d85e-07f0-4962-a78b-ab1bfe39c6d8',
        'client_secret': 'APOO8c_OjK4DrcwoTYp82KUv2LrRvD_hlVinoZzqoxO5EPUZhprbb4azfXp8qTdMFxdviSQIKr7SMswVpR4SSVc',
        'service_root': 'https://sb-fhir-dstu2.smarthealthit.org/smartdstu2/data',
    },
    'public': {
        'client_id': 'c4be90c5-6076-4253-8bf5-2c1aa5ce8598',
        'service_root': 'https://sb-fhir-dstu2.smarthealthit.org/smartdstu2/data',
    },
    'cerner': {
        # 'client_id': '4f769b4c-36de-44dd-aa40-58d1100633f8',
        'client_id': '7f05b4e4-72c0-482b-95d6-6325aabf0aef',
        'service_root': 'https://fhir-myrecord.sandboxcerner.com/dstu2/0b8a0111-e8e6-4c26-a91c-5069cbc6b1ca',
        'scope': ' '.join([
            'profile',
            'openid',
            'online_access',
            'patient/AllergyIntolerance.read',
            'patient/Appointment.read',
            'patient/Binary.read',
            'patient/CarePlan.read',
            'patient/Condition.read',
            'patient/Contract.read',
            'patient/Device.read',
            'patient/DiagnosticReport.read',
            'patient/DocumentReference.read',
            'patient/Encounter.read',
            'patient/Goal.read',
            'patient/Immunization.read',
            'patient/MedicationAdministration.read',
            'patient/MedicationOrder.read',
            'patient/MedicationStatement.read',
            'patient/Observation.read',
            'patient/OperationDefinition.read',
            'patient/Patient.read',
            'patient/Person.read',
            'patient/Practitioner.read',
            'patient/Procedure.read',
            'patient/RelatedPerson.read',
            'patient/Schedule.read',
            'patient/Slot.read',
            'patient/StructureDefinition.read',
            'patient/Appointment.write'])
    }
}

JWT_SECRET = 'itsaseekrit'
SERVICE_ROOT = 'https://sb-fhir-dstu2.smarthealthit.org/smartdstu2/data'
SCOPE = 'launch patient/*.* openid profile offline_access'
SCOPE += ' launch/patient'


@app.route('/ehr/<client>/launch')
def launch(client):
    iss = request.args['iss']
    launch = request.args.get('launch', None)
    conn = Connection(iss)
    md = conn.metadata
    service = md.rest[0]

    state = auth.jwt_state(JWT_SECRET)
    config = CLIENTS[client]

    authorization_url, state = auth.authorization_url(
        service,
        client_id=config['client_id'],
        client_secret=config.get('client_secret'),
        redirect_uri=url_for('callback', client=client, _external=True),
        scope=config.get('scope', SCOPE) + ' launch',
        state=state,
        launch=launch)
    print(authorization_url)

    return redirect(authorization_url)


@app.route('/ehr/<client>/callback')
def callback(client):
    config = CLIENTS[client]
    conn = Connection(config['service_root'])
    md = conn.metadata
    service = md.rest[0]
    token = auth.fetch_token(
        service,
        client_id=config['client_id'],
        client_secret=config.get('client_secret'),
        redirect_uri=url_for('callback', client=client, _external=True),
        authorization_response=request.url,
        state_validator=auth.jwt_state_validator(JWT_SECRET))
    config['token'] = token
    return jsonify(token)


@app.route('/ehr/<client>/token')
def token(client):
    config = CLIENTS[client]
    return jsonify(config['token'])