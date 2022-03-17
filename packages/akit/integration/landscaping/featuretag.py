
class FeatureTagNodeMeta(type):

    def __new__(metacls, name, bases, namespace, **kwargs):
        cls = super().__new__(metacls, name, bases, namespace, **kwargs)
        cls.ID = cls.__qualname__.lower().replace(".", "/")
        return cls
    
    def __repr__(self):
        return "'{}'".format(self.ID)

class FeatureTag(metaclass=FeatureTagNodeMeta):
    ID = None