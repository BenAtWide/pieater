# feed eater
import os
import sys
import feedparser
import requests
from datetime import datetime, timedelta

rss_feed = "https://www.theguardian.com/uk/rss"

location=('50.8425', '-0.135')

try:
    wu_apikey = os.environ['WU_APIKEY']
except KeyError:
    sys.exit("Set WU_APIKEY environment variable")
    
cached =[]
wu_url = "http://api.wunderground.com/api/{}/conditions/q/{},{}.json".format(wu_apikey, location[0], location[1])
wu_forecast = "http://api.wunderground.com/api/{}/forecast/q/{},{}.json".format(wu_apikey, location[0], location[1])


class BaseData(object):
    """Base class for feeds"""
    def __init__(self, feedurl, **kwargs):
        super(BaseData, self).__init__()
        self.feedurl = feedurl
        self.kwargs = kwargs
        self.update_interval = 15
        self.last_update = None
        self.raw_data = None
        
    def fetch_updates(self):
        """ Get the latest feed data, and store in raw_data """
        raise NotImplemented
        
    def needs_update(self):
        """ Is it time to fetch updates?"""
        if not self.last_update:
            return True
        now = datetime.now()
        if self.last_update + timedelta(minutes=self.update_interval) < now:
            return True
        else:
            return False
        
    def update(self):
        if self.needs_update:
            self.fetch_updates()
    
    def data_string(self):
        """ The formatted string to display """
        return ''
        
    def data_list(self):
        """ A list of formatted strings, if there are multiple items"""
        return []

class NewsFeed(BaseData):
    """ News from the Grauniad"""
    def __init__(self, *args, **kwargs):
        super(NewsFeed, self).__init__(*args, **kwargs)
        self.etag = ''
        self.entry_count = kwargs.get('entry_count', 10)
    
    def fetch_updates(self):
        if self.etag:
            fd = feedparser.parse(rss_feed, etag=self.etag)
            if fd.status == 304:
                return
        else:
            fd = feedparser.parse(rss_feed)
            if fd.etag:
                self.etag = fd.etag
            self.last_update = datetime.now()
            self.raw_data = fd.entries[0:self.entry_count]                    
            
    def data_list(self):
        """ Return the titles from our news story list."""
        return [e.title for e in self.raw_data]
        


class WeatherFeed(BaseData):
    """ Get the latest weather """
    
    def fetch_updates(self):
        r=requests.get(self.feedurl)
        arr = r.json()
        weather = arr.get('current_observation', None)
        if not weather:
            print "Could not get weather from feed"
        self.raw_data = weather
        self.last_update = datetime.now()

    def data_string(self):
        return "{}, {}C".format(self.raw_data['weather'], self.raw_data['temp_c'])        
    



