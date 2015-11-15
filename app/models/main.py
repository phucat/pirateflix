from ferris import BasicModel, ndb
import logging


class Main(BasicModel):

    criteria = ndb.StringProperty()
    data = ndb.JsonProperty()
    permissions = ndb.JsonProperty()
    resolved = ndb.BooleanProperty()

    @classmethod
    def create(cls, params):
        entity = cls.get(params['criteria'])
        if entity:
            return entity

        item = cls(id=params['criteria'])
        item.populate(**params)
        item.put()
        return item

    @classmethod
    def get(cls, key_name, key_only=False):
        if not key_name:
            return None
        key = ndb.Key(cls, key_name)
        ret = key.get()
        if key_only:
            return key if ret else None
        return ret
