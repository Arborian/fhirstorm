from ..util import reify

from .base_resource import Resource
from .service import Service


@Resource.register_resource('Conformance')
class Conformance(Resource):

    @property
    def rest(self):
        return [
            Service(it, _bind=self.bind)
            for it in self['rest']]


@Resource.register_resource('CapabilityStatement')
class CapabilityStatement(Resource):

    @property
    def rest(self):
        return [
            Service(it, _bind=self.bind)
            for it in self['rest']]

