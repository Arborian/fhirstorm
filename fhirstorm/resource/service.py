from .base_resource import Resource

from ..util import AttrProxy


@Resource.register_resource('_Service')
class Service(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._registry = {}
        self.r = ResourceCollection(self)

    @property
    def security(self):
        return Security(self['security'], _bind=self.bind)

    def resourceClass(self, name, **metadata):
        result = self._registry.get(name)
        if result is not None:
            return result
        base_cls = Resource.resourceClass(name)
        result = self._registry[name] = type(
            name, (base_cls,), {'metadata': metadata})
        return result


    def refresh_token(self):
        if self.bind.client_secret:
            auth = (self.bind.session.client_id, self.bind.client_secret)
        else:
            auth = None
        new_token = self.bind.session.refresh_token(
            self.security.oauth2_uris.token,
            auth=auth)
        return new_token


class ResourceCollection(dict):

    def __init__(self, service):
        super().__init__({
            res['type']: service.resourceClass(
                res['type'], bind=service.bind, **res)
            for res in service.resource})
        self._service = service

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __dir__(self):
        return list(self)


@Resource.register_resource('_Security')
class Security(Resource):

    @property
    def oauth2_uris(self):
        for ext in self.extension:
            if ext['url'] == 'http://fhir-registry.smarthealthit.org/StructureDefinition/oauth-uris':
                return Oauth2Uris(
                    {e.url: e.valueUri for e in ext.extension},
                    _bind=self.bind)


class Oauth2Uris(Resource):
    resourceType = '_Oauth2Uris'
