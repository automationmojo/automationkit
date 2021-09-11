
class FeatureNodeMeta(type):
    def __new__(metacls, name, bases, namespace, **kwargs):
        cls = super().__new__(metacls, name, bases, namespace, **kwargs)
        cls.ID = cls.__qualname__.lower().replace(".", "/")
        return cls

class FeatureNode(metaclass=FeatureNodeMeta):
    ID = None
