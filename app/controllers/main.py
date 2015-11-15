from google.appengine.api import users
from ferris import Controller, route, messages, scaffold
from ferris.components.search import Search
from ferris.core import search
from ferris.components.pagination import Pagination
from google.appengine.ext import deferred
from google.appengine.api import urlfetch

from app.models.main import Main
import logging
import urllib2


class Main(Controller):
    class Meta:
        # authorizations = (require_user,)
        prefixes = ('api', 'admin')
        Model = Main
        pagination_limit = 20
        components = (scaffold.Scaffolding, Search, Pagination, messages.Messaging)

    @route
    def api_test(self):
        # content = urllib2.urlopen("https://thepiratebay.gd/browse/201/0/7/0").read()
        # return content
        url = "https://thepiratebay.gd/browse/201/0/7/0"
        sttweets = urlfetch.fetch(url, validate_certificate=False)
        stcode = sttweets.status_code

        if stcode == 200:
            return sttweets.content
            stresults = json.loads(sttweets.content, 'utf-8')
            return stresults