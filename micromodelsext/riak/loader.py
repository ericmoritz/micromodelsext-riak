
class Loader(object):
    def __init__(self, bucket, model_cls):
        self._model_cls = model_cls
        self._bucket = bucket

    def cast(self, obj):
        """Cast a RiakObject into the provided model"""
        return self._model_cls.from_dict(obj.get_data())

    def __getitem__(self, key):
        """Get a model using a key"""
        obj = self._bucket.get(key)

        if not obj.exists():
            raise KeyError()
        else:
            return self.cast(obj)
        
    def __setitem__(self, key, model):
        """Set a model under a key"""
        obj = self._bucket.new(key, data=model.to_dict(serial=True))
        obj.store()

    def __delitem__(self, key):
        obj = self._bucket.get(key)
        if not obj.exists(): raise KeyError()
        obj.delete()

        
