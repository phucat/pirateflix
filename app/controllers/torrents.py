from google.appengine.api import users
from ferris import Controller, route, messages, scaffold, route_with
from ferris.components.search import Search
from ferris.core import search
from ferris.components.pagination import Pagination
from google.appengine.ext import deferred
from google.appengine.api import urlfetch

from app.models.torrent import Torrent
from app.components.magnet2torrent import magnet2torrent
import datetime
import transmissionrpc
import logging
import urllib2

DOWNLOAD_DIR = '/var/lib/transmission-daemon/downloads/'
logging.getLogger('transmissionrpc').setLevel(logging.DEBUG)
tc = transmissionrpc.Client('localhost', port=9091, user="transmission", password="transmission")


class Torrents(Controller):
    class Meta:
        # authorizations = (require_user,)
        prefixes = ('api', 'admin')
        Model = Torrent
        pagination_limit = 20
        # components = (scaffold.Scaffolding, Search, Pagination, messages.Messaging)

    def get_info(self, torrent):
        item = {
            'hashString': torrent.hashString,
            'name': torrent.name,
            'status': torrent.status,
            'eta': datetime.datetime.now() + torrent.eta
        }
        return item

    @route
    def api_list(self):
        torrents = tc.get_torrents()
        items = []
        for t in torrents:
            item = self.get_info(t)
            items.append(item)
            Torrent.create(item)
        return self.util.stringify_json(items)

    @route_with('/api/torrents/add/<magnet_link>')
    def api_add(self, magnet_link):
        torrent = magnet2torrent("magnet:?xt=urn:btih:49fbd26322960d982da855c54e36df19ad3113b8&dn=ubuntu-12.04-desktop-i386.iso&tr=udp%3A%2F%2Ftracker.openbittorrent.com", 'new')
        try:
            tc.add_torrent(torrent)
            return 200
        except:
            return 501

    @route_with('/api/torrents/remove/<id>')
    def api_remove(self, id):
        # tc.stop_torrent(1)
        tc.remove_torrent(id, delete_data=True)
        return 200