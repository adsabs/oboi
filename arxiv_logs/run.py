
import os
from datetime import datetime
import time
from adsputils import load_config, setup_logging
import gzip

class InfluxDbConsumer():
    def consume(self, date, key, value):
        ts = time.mktime(date.utctimetuple())
        self._post(timestamp=ts, key=key)
        
    def _post(self, **kwargs):
        self.client.post(data=kwargs)


class ALapp():
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
        self._config = load_config(extra_frames=1, proj_home=proj_home, app_name=app_name)

        local_config = None
        if 'local_config' in kwargs and kwargs['local_config']:
            local_config = kwargs.pop('local_config')
            self._config.update(local_config) #our config
        if not proj_home:
            proj_home = self._config.get('PROJ_HOME', None)
        self.logger = setup_logging(app_name, proj_home=proj_home,
                                    level=self._config.get('LOGGING_LEVEL', 'INFO'),
                                    attach_stdout=self._config.get('LOG_STDOUT', False))

        
    def process_folder(self, src):
        for root, dirs, files in os.walk(src):
            for name in files:
                fn = os.path.join(root, name)
                found = False
                for p in self.valid_file_patterns:
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
                bibcode, reader = '\t'.split(l)
                consumer.consume(dayoflog, bibcode, reader)
        finally:
            fin.close()
                
        