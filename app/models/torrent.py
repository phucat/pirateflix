from ferris import BasicModel, ndb
import logging


class Torrent(BasicModel):

    hashString = ndb.StringProperty()
    name = ndb.StringProperty()
    status = ndb.StringProperty()
    eta = ndb.DateTimeProperty()

    @classmethod
    def create(cls, params):
        entity = cls.get(params['hashString'])
        if entity:
            item = entity
        else:
            item = cls(id=params['hashString'])
            
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
