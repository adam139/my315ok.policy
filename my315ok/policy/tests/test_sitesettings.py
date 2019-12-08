#-*- coding: UTF-8  -*-
import unittest
from my315ok.policy.testing import INTEGRATION_TESTING

from Products.CMFCore.utils import getToolByName

class TestSetup(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    
    def test_portal_title(self):
        portal = self.layer['portal']
        self.assertEqual("易智网站系统", portal.getProperty('title'))
    
    def test_portal_description(self):
        portal = self.layer['portal']
        self.assertEqual("大同网络科技有限公司EZsite——基于部件体型架构的网站系统", portal.getProperty('description'))

    

