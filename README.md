# FHIRstorm

## SMART on FHIR for Python

You know, because SMART on FHIR is the name of the protocol

... and Firestorm is a DC hero who's basically a really smart guy

... who is on fire.

Also, I couldn't easily find any puns having to do with intelligent snakes
on fire.

## Getting started

### Obtain FHIRstorm:

```
pip install fhirstorm
```

### Obtain app credentials from a SMART on FHIR installation:

You can get free sandbox credentials from one of the following:

- [SMART on FHIR SmartHealthIT Sandbox][smarthealthit]
- [Healthcare Services Platform Consortium Sandbox][hspc]
- [Open Epic][epic]
- [Cerner Millenium][cerner]
- [Allscripts][allscripts]

[smarthealthit]: http://docs.smarthealthit.org/
[hspc]: https://sandbox.hspconsortium.org/
[epic]: https://open.epic.com/
[cerner]: http://fhir.cerner.com/millennium/dstu2/
[allscripts]: https://developer.allscripts.com/

You'll need to be ready with a `redirect_url` when you sign up (this
is where you'll receive the OAuth2 callback that gives you a code that
you'll exchange for an authorization token.)

### Obtain an authorization code

```python
import os
from fhirstorm import Connection, auth

# Replace with the service root of your SMART on FHIR endpoint
SERVICE_ROOT = 'https://sb-fhir-stu3.smarthealthit.org/smartstu3/data'
CLIENT_ID = '<you get this when you register your app>'
REDIRECT_URI = '<YOUR OWN url, to which the FHIR endpoint will redirect the user>'
CLIENT_SECRET = '<you *might* get one of these when you register your app>'
INTERNAL_SECRET = 'itsaseekrit' # please do better than this

# You need this if you used a `http://localhost...` redirect url
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

conn = Connection(SERVICE_ROOT)

# Get the particular REST endpoint (there's usually just the one)
service = conn.metadata.rest[0]

# Get your authorization url
authorization_url, state = auth.authorization_url(
    service,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope='profile openid offline_access launch/patient patient/*.*',
    state=auth.jwt_state(INTERNAL_SECRET),
    aud=SERVICE_ROOT)
```

Now, send the user to the URL you just got.
Best practice is for you to also save the `state` variable somewhere safe, and
verify that the identical state is passed back to you.
In this example, however, I'll do the less-safe "verify that some valid signed
JWT was passed back to you."

The user will be redirected back to you redirect_uri after they log in (sandbox
credentials are different for each of the sandboxes; consult their documentation
for the correct credentials to use when logging in)

### Obtain an authorization token

Once you have received the callback, use the *whole URL* you received (it should include
a state and code parameter, at a minimum):

```python
# Assuming you've stored the actual redirect URL received into authorization response...

tok = auth.fetch_token(
    service, CLIENT_ID, REDIRECT_URI,
    authorization_response,
    client_secret=CLIENT_SECRET,        # if you have one, otherwise leave it off
    state_validator=auth.jwt_state_validator(INTERNAL_SECRET))

# Or if you saved the state:
tok = auth.fetch_token(
    service, CLIENT_ID, REDIRECT_URI,
    authorization_response,
    client_secret=CLIENT_SECRET,        # if you have one, otherwise leave it off
    state=STATE_VALUE_YOU_SAVED)

```

Now you can use this token to access the various FHIR resources. Save it somewhere safe.

```python
conn = Connection(
    SERVICE_ROOT,
    session=OAuth2Session(
        client_id=CLIENT_ID, token=token))

service = connection.metadata.rest[0]
```

In many of the implementations, you'll get the patient ID right in the token. Sometimes, it
comes (in JWT form!) inside the encoded access token:

```python
import jwt

patient_id = token.get('patient')
if patient_id is None:
    decoded = jwt.decode(token['access_token'], verify=False)
    patient_id = decoderd.get('local_patient_id')
```

Once you've been authorized, though, you can get resources off the `service.r` object:

```python
# Fetch the patient
p = service.r.Patient.fetch(patient_id)

# Get all medication orders for the patient
res = service.r.MedicationOrder.search(dict(patient=p.id))

```

### What next?

Now that you've gotten started, you can check out the Jupyter Notebook [tutorials][tutorials] for more detail.

Get FHIRing!

[tutorials]: ./notebooks

