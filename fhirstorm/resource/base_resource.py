from urllib.parse import urlencode

class Resource(dict):
    _registry = {}
    metadata = {}
    resourceType = ''

    def __init__(self, *args, **kwargs):
        self.bind = kwargs.pop('_bind', None)
        if self.bind is None:
            self.bind = self.metadata.get('bind')
        super().__init__(*args, **kwargs)

    def __repr__(self):
        bound = 'Bound' if self.bind else 'Unbound'
        if self.resourceType:
            return f'<{bound} {self.resourceType}>'
        else:
            return super().__repr__()

    @classmethod
    def search(cls, spec, bind=None):
        if bind is None:
            bind = cls.metadata.get('bind')
        qs = urlencode(spec, doseq=True)
        resp = bind.get(f'/{cls.resourceType}?{qs}')
        return cls.from_dict(resp, bind=bind)

    @classmethod
    def fetch(cls, id, bind=None):
        if bind is None:
            bind = cls.metadata.get('bind')
        resp = bind.get(f'/{cls.resourceType}/{id}')
        return cls.from_dict(resp, bind=bind)

    @classmethod
    def register_resource(cls, resourceType):
        def decorator(subclass):
            subclass.resourceType = resourceType
            cls._registry[resourceType] = subclass
            return subclass
        return decorator

    @classmethod
    def resourceClass(cls, name, **metadata):
        result = cls._registry.get(name)
        if result is not None:
            return result
        result = cls._registry[name] = type(
            name, (Resource,),
            {'resourceType': name, 'metadata': metadata})
        return result

    @classmethod
    def from_dict(cls, dct, resourceType=None, bind=None):
        if resourceType is None:
            resourceType = dct.get('resourceType', '')
        dct = {
            key: _make_resources(value, bind=bind)
            for key, value in dct.items()}
        resourceClass = cls.resourceClass(resourceType)
        return resourceClass(dct, _bind=bind)

    def resolve(self):
        return self.from_dict(
            self.bind.get(f'/{self.reference}'),
            bind=self.bind)

    def __dir__(self):
        return [*super().__dir__(), *self.keys()]

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


def _make_resources(obj, bind=None):
    if isinstance(obj, list):
        return [_make_resources(item, bind=bind) for item in obj]
    elif isinstance(obj, dict):
        return Resource.from_dict(obj, bind=bind)
    else:
        return obj
