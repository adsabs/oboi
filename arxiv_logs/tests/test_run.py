'''
Created on Nov 20, 2018

@author: rchyla
'''
import sys
print sys.path
import unittest
from arxiv_logs import app
import os
from mock import patch, MagicMock,call
import datetime

class Test(unittest.TestCase):


    def setUp(self):
        
        self.app = app.ArxivLogApplication('test')


    def tearDown(self):
        if hasattr(self.app, 'close'):
            self.app.close()
        self.app = None


    def test_process(self):
        d = os.path.dirname(__file__)
        consumer = MagicMock()
        with patch.object(self.app, '_get_consumer', return_value=consumer):
            self.app.process_folder(d)
            assert consumer.consume.call_count == 120
            assert consumer.consume.call_args == call(datetime.datetime(2018, 11, 3, 0, 0), '0704.0362', 'X56d9e101f')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()