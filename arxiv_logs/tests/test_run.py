'''
Created on Nov 20, 2018

@author: rchyla
'''
import unittest
from arxiv_logs import app
import os

class Test(unittest.TestCase):


    def setUp(self):
        self.app = app.ArxivLogApplication('test')


    def tearDown(self):
        if hasattr(self.app, 'close'):
            self.app.close()
        self.app = None


    def test_process(self):
        d = os.path.dirname(__file__)
        self.app.process_folder(d)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()