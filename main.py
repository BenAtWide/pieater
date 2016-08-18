# PiEater. Runs the Pimoroni status display.
# main script, run by supervisord
from feeds import NewsFeed, WeatherFeed

try:
    import dothat.lcd as lcd
except ImportError:
    lcd = None
    
    
if not lcd:
    print "no lcd module"
    

