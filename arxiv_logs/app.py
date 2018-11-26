import os
from datetime import datetime
import time
from adsputils import load_config, setup_logging, date2solrstamp
import gzip
from influxdb import InfluxDBClient

class InfluxDbConsumer():
    def __init__(self, config):
        host = config.get('HOST', 'localhost')
        port = config.get('PORT', 8086)
        user = config.get('USER', None)
        passwd = config.get('PASSWD', None)
        dbname = config.get('DATABASE', 'arxiv_logs')
        self.client = InfluxDBClient(host, port, user, passwd, dbname)
        self.client.create_database(dbname)
        
    def consume(self, date, key, value):
        json_body = [
            {
                "measurement": "reads",
                "tags": {
                    "host": "arxiv",
                    "paper": key
                },
                "time": date2solrstamp(date),
                "fields": {
                    "Int_value": 1,
                    "String_value": value
                }
            }
        ]
        self.client.write_points(json_body)
        
        #ts = time.mktime(date.utctimetuple())
        #self._post(timestamp=ts, key=key, value=)
        
    def _post(self, **kwargs):
        self.client.post(data=kwargs)


class ArxivLogApplication():
    """
    """

    def __init__(self, app_name, *args, **kwargs):
        """
        :param: app_name - string, name of the application (can be anything)
        :keyword: local_config - dict, configuration that should be applied
            over the default config (that is loaded from config.py and local_config.py)
        """
        proj_home = None
        if 'proj_home' in kwargs:
            proj_home = kwargs.pop('proj_home')
        self.config = load_config(extra_frames=1, proj_home=proj_home, app_name=app_name)

        local_config = None
        if 'local_config' in kwargs and kwargs['local_config']:
            local_config = kwargs.pop('local_config')
            self.config.update(local_config) #our config
        if not proj_home:
            proj_home = self.config.get('PROJ_HOME', None)
        self.logger = setup_logging(app_name, proj_home=proj_home,
                                    level=self.config.get('LOGGING_LEVEL', 'INFO'),
                                    attach_stdout=self.config.get('LOG_STDOUT', False))
        
    @property
    def consumer(self):
        return self._get_consumer()
        
    
    def _get_consumer(self):
        c = self.config.get('CONSUMER', 'influxdb').lower()
        if 'influx' in c:
            return InfluxDbConsumer(self.config)
        else:
            raise Exception('Unknown conumer: %s' % c)
        
    def process_folder(self, src):
        for root, dirs, files in os.walk(src):
            for name in files:
                fn = os.path.join(root, name)
                found = False
                for p in self.config.get('VALID_FILE_PATTERNS', ['.log.gz', '.log']):
                    if p in fn:
                        found = True
                        break
                if not found:
                    continue
                self.process_file(fn, self.consumer)
                
    
    def process_file(self, f, consumer):
        bn = os.path.basename(f)
        dayoflog = datetime.strptime(bn[0:6], '%y%m%d')
        try:
            if '.gz' in f:
                fin = gzip.open(f, 'rb')
            else:
                fin = open(f, 'r')
        
            for l in fin:
                l = l.strip()
                if not l:
                    continue
                bibcode, reader = l.split()
                consumer.consume(dayoflog, bibcode, reader)
        except Exception, e:
            self.logger.error("Error reading data from %s", bn)
            self.logger.error(e)
        finally:
            if fin:
                fin.close()
                
