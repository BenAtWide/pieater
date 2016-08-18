# feed eater

import feedparser
import requests
from datetime import datetime, timedelta

rss_feed = "https://www.theguardian.com/uk/rss"
# rss_feed = "/Users/ben/Dropbox/webapps/pieater/testfeed.xml"
rss_etag = None
rss_interval = timedelta(minutes=15)


location=('50.8425', '-0.135')
wu_apikey ='bfb306c6d72a37c6'
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
        r=requests.get(wu_url)
        arr = r.json()
        weather = arr.get('current_observation', None)
        if not weather:
            print("Could not get weather from feed")
        self.raw_data = weather
        self.last_update = datetime.now()

    def data_string(self):
        return "{}, {}C".format(self.raw_data['weather'], self.raw_data['temp_c'])        
    
rss_updated = datetime.now() - timedelta(minutes=20)    
# print(fetch_rss_feed(rss_updated, rss_feed, rss_etag))
#print(fetch_weather('now'))

# gfeed = NewsFeed("https://www.theguardian.com/uk/rss")


"""{'response': 
        {'features': 
            {'conditions': 1}, 
            'version': '0.1', 
            'termsofService': 'http://www.wunderground.com/weather/api/d/terms.html'}, 
            'current_observation': 
                {'wind_mph': 3.7, 'precip_1hr_in': '-999.00', 'nowcast': '', 'weather': 'Partly Cloudy', 'windchill_string': 'NA', 'wind_kph': 6.0, 'pressure_in': '29.89', 'windchill_c': 'NA', 'wind_string': 'From the SSE at 3.7 MPH Gusting to 10.6 MPH', 'pressure_trend': '0', 'wind_gust_kph': '17.1', 'wind_gust_mph': '10.6', 'observation_time': 'Last Updated on August 17, 2:11 PM BST', 'local_time_rfc822': 'Wed, 17 Aug 2016 14:20:35 +0100', 'local_epoch': '1471440035', 'precip_today_string': '-999.00 in (-25375 mm)', 'local_tz_long': 'Europe/London', 'feelslike_f': '81', 'ob_url': 'http://www.wunderground.com/cgi-bin/findweather/getForecast?query=50.844360,-0.136445', 'solarradiation': '--', 'observation_epoch': '1471439514', 'feelslike_c': '27', 'display_location': {'state_name': 'United Kingdom', 'elevation': '108.00000000', 'country_iso3166': 'GB', 'city': 'Brighton and Hove', 'full': 'Brighton and Hove, United Kingdom', 'magic': '13', 'longitude': '-0.130000', 'latitude': '50.840000', 'zip': '00000', 'state': '', 'country': 'UK', 'wmo': 'WBRIG'}, 'dewpoint_c': 17, 'precip_today_metric': '--', 'dewpoint_f': 62, 'precip_1hr_metric': ' 0', 'feelslike_string': '81 F (27 C)', 'temperature_string': '79.3 F (26.3 C)', 'temp_c': 26.3, 'wind_degrees': 167, 'observation_time_rfc822': 'Wed, 17 Aug 2016 14:11:54 +0100', 'pressure_mb': '1012', 'relative_humidity': '55%', 'dewpoint_string': '62 F (17 C)', 'heat_index_string': '81 F (27 C)', 'station_id': 'IBRIGHTO43', 'observation_location': {'latitude': '50.844360', 'country': 'UK', 'elevation': '305 ft', 'country_iso3166': 'GB', 'state': '', 'city': 'Hythe Road, Brighton', 'full': 'Hythe Road, Brighton, ', 'longitude': '-0.136445'}, 'icon': 'partlycloudy', 'heat_index_c': 27, 'precip_today_in': '-999.00', 'heat_index_f': 81, 'precip_1hr_string': '-999.00 in ( 0 mm)', 'local_tz_offset': '+0100', 'forecast_url': 'http://www.wunderground.com/global/stations/WBRIG.html', 'image': {'url': 'http://icons.wxug.com/graphics/wu2/logo_130x80.png', 'title': 'Weather Underground', 'link': 'http://www.wunderground.com'}, 'local_tz_short': 'BST', 'UV': '7', 'temp_f': 79.3, 'visibility_km': '10.0', 'estimated': {}, 'history_url': 'http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=IBRIGHTO43', 'wind_dir': 'SSE', 'windchill_f': 'NA', 'visibility_mi': '6.2', 'icon_url': 'http://icons.wxug.com/i/c/k/partlycloudy.gif'}}"""