import ConfigParser
import os
import time
from astral import Astral
from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet import task
from houseagent import config_to_location
from houseagent.plugins import pluginapi
from houseagent.plugins.pluginapi import Logging

# Fix to support both twisted.scheduling and txscheduling (new version)
try:
    from txscheduling.cron import CronSchedule
    from txscheduling.task import ScheduledCall      
except ImportError:
    from twisted.scheduling.cron import CronSchedule
    from twisted.scheduling.task import ScheduledCall    


class AstralWrapper(object):

    def __init__(self):
        '''
        Load initial Astral configuration from Astral.conf
        '''   
        config_file = config_to_location('Astral.conf')
        
        self.config = ConfigParser.RawConfigParser()
        self.config.read(os.path.join(config_file))

        # Get broker information (ZeroMQ)
        self.coordinator_host = self.config.get("coordinator", "host")
        self.coordinator_port = self.config.getint("coordinator", "port")
        
        self.loglevel = self.config.get('general', 'loglevel')
        self.log = Logging("Astral", console=True)
        self.log.set_level(self.loglevel)
        
        self.id = self.config.get('general', 'id')
        callbacks = {}
        self.pluginapi = pluginapi.PluginAPI(self.id, 'Astral', 
                                             broker_host=self.coordinator_host, 
                                             broker_port=self.coordinator_port,
                                             **callbacks)
        self.pluginapi.ready()
        
        c = CronSchedule("* * * * *")
        s = ScheduledCall(f=self.fire_minute)
        s.start(c)
                                
        reactor.run()
        return True
    
    def fire_minute(self):
        city = Astral()[self.config.get("astral", "city")]
        sun = city.sun()
        self.log.debug(sun)

        delta = int(time.time()) - int(time.mktime(sun["sunrise"].timetuple())) + 30
        if delta > 0:
            self.log.info("Sunrise was {0} minutes ago".format(delta // 60))
        else:
            self.log.info("Sunrise in {0} minutes".format(-(delta // 60)))
        self.pluginapi.value_update("1", {"Sunrise delta": delta // 60})

        delta = int(time.time()) - int(time.mktime(sun["sunset"].timetuple())) + 30
        if delta > 0:
            self.log.info("Sunset was {0} minutes ago".format(delta // 60))
        else:
            self.log.info("Sunset in {0} minutes".format(-(delta // 60)))
        self.pluginapi.value_update("1", {"Sunset delta": delta // 60})
        
        delta = int(time.time()) - int(time.mktime(sun["dawn"].timetuple())) + 30
        if delta > 0:
            self.log.info("Dawn was {0} minutes ago".format(delta // 60))
        else:
            self.log.info("Dawn in {0} minutes".format(-(delta // 60)))
        self.pluginapi.value_update("1", {"Dawn delta": delta // 60})
        
        delta = int(time.time()) - int(time.mktime(sun["dusk"].timetuple())) + 30
        if delta > 0:
            self.log.info("Dusk was {0} minutes ago".format(delta // 60))
        else:
            self.log.info("Dusk in {0} minutes".format(-(delta // 60)))
        self.pluginapi.value_update("1", {"Dusk delta": delta // 60})
        
        delta = int(time.time()) - int(time.mktime(sun["noon"].timetuple())) + 30
        if delta > 0:
            self.log.info("Solar noon was {0} minutes ago".format(delta // 60))
        else:
            self.log.info("Solar noon in {0} minutes".format(-(delta // 60)))
        self.pluginapi.value_update("1", {"Solar noon delta": delta // 60})

    
if os.name == 'nt':        
    class AstralService(pluginapi.WindowsService):
        '''
        This class provides a Windows Service interface for the Astral plugin.
        '''
        _svc_name_ = "haAstral"
        _svc_display_name_ = "HouseAgent - Astral Service"
        
        def start(self):
            '''
            Start the Astral interface.
            '''
            AstralWrapper()
        
if __name__ == '__main__':
    if os.name == 'nt':
        # We want to start as a Windows service on Windows.
        pluginapi.handle_windowsservice(AstralService) 
    else:
        AstralWrapper()