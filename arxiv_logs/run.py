
import os
from datetime import datetime
import time

class InfluxDbConsumer():
    def consume(self, date, key, value):
        ts = time.mktime(date.utctimetuple())
        self._post(timestamp=ts, key=key)
        
    def _post(self, **kwargs):
        self.client.post(data=kwargs)

def process_file(f, consumer):
    bn = os.path.basename(f)
    dayoflog = datetime.strptime(bn[0:6], '%y%m%d')
    with open(f, 'r') as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            bibcode, reader = '\t'.split(l)
            consumer.consume(dayoflog, bibcode, reader)
            