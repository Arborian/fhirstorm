import copy
from .util import reify

import requests
from requests_oauthlib import OAuth2Session
from .resource import Resource


class Connection:

    def __init__(self, service_root, session=None, client_secret=None):
        self.service_root = service_root.rstrip('/')
        if session is None:
            session = OAuth2Session()
        self.session = session
        self.client_secret = client_secret
        self.session.headers['Accept'] = 'application/json'

    def __repr__(self):
        return f'<Connection {self.service_root}>'

    @classmethod
    def from_token(cls, service_root, token):
        session = OAuth2Session(token=token)
        self = cls(service_root, session=session)

    @reify
    def metadata(self):
        url = self.service_root + '/metadata'
        resp = requests.get(url, headers={'Accept': 'application/json'})
        resp.raise_for_status()
        return resp.json()

    def service(self, rest_id=0):
        return Resource.from_dict(
            self.metadata['rest'][rest_id],
            resourceType='_Service',
            bind=self)

    def get(self, path):
        url = self.service_root + path
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def clone(self, **kwargs):
        result = copy.copy(self)
        for k, v in kwargs.items():
            setattr(result, k, v)
        return result
