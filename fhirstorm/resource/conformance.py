from barin.util import reify

from .base_resource import Resource


@Resource.register('Conformance')
class Conformance(Resource):

    @property
    def rest(self):
        return [
            RestEndpoint(it, _bind=self.bind)
            for it in self['rest']]


@Resource.register('CapabilityStatement')
class CapabilityStatement(Resource):

    @property
    def rest(self):
        return [
            RestEndpoint(it, _bind=self.bind)
            for it in self['rest']]


class ResourceCollection(Resource):
    resourcetype = '_ResourceCollection'


class RestEndpoint(Resource):
    resourceType = '_RestEndpoint'

    @reify
    def supported_resources(self):
        return [
            self.resourceClass(res.type)
            for res in self.resource]

    @reify
    def security(self):
        return Security(self['security'], _bind=self.bind)

    @reify
    def r(self):
        return ResourceCollection({
            res.type: self.resourceClass(
                res.type, bind=self.bind, **res)
            for res in self.resource
        }, _bind=self.bind)

    def refresh_token(self):
        if self.bind.client_secret:
            auth = (self.bind.session.client_id, self.bind.client_secret)
        else:
            auth = None
        new_token = self.bind.session.refresh_token(
            self.security.oauth2_uris.token,
            client_secret=self.bind.client_secret,
            auth=auth)
        return new_token


class Security(Resource):
    resourceType = '_Security'

    @property
    def oauth2_uris(self):
        for ext in self.extension:
            if ext.url == 'http://fhir-registry.smarthealthit.org/StructureDefinition/oauth-uris':
                return Oauth2Uris(
                    {e.url: e.valueUri for e in ext.extension},
                    _bind=self.bind)


class Oauth2Uris(Resource):
    resourceType = '_Oauth2Uris'
