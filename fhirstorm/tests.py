import os
import unittest

import yaml
from fhirey import Connection, auth


def load_config():
    with open('../cf-api/config/smart.yaml') as fp:
        smart_config = yaml.load(fp)
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
    cerner = smart_config['dev']['cerner']
    cerner['redirect_uri'] = 'http://localhost:3000/smart/cerner/redirect'
    return cerner


class TestAuth(unittest.TestCase):

    def testAuth(self):
        cerner = load_config()
        conn = Connection(cerner['service_root'])
        print(conn.metadata)
        print(conn.metadata.rest)
        service = conn.metadata.rest[0]
        print(service)
        rv = auth.authorization_url(
            service,
            client_id=cerner['client_id'],
            redirect_uri=cerner['redirect_uri'],
            scope=' '.join(cerner['scope']),
            state='123')
        print(rv)

if __name__ == '__main__':
    unittest.main()
