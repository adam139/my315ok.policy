#-*- coding: UTF-8 -*-
import unittest
import transaction
from datetime import date
from datetime import datetime
from plone.testing.z2 import Browser
from zope import event

from my315ok.policy.testing import FUNCTIONAL_TESTING,INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID,TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import setRoles,login,logout
from plone.app.textfield.value import RichTextValue

class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
    def setUp(self):   
        portal = self.layer['portal']
        app = self.layer['app']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        setRoles(portal, TEST_USER_ID, ('Manager',))               
 
        portal.invokeFactory('my315ok.policy.blogfolder', 'folder')
        portal['folder'].invokeFactory('my315ok.policy.blog', 'doc',
                                       title="title",
                                       description=u"description",
                                       text=RichTextValue(            u"here is rich text",
                                                                       'text/plain',
                                                                       'text/html'
                                                                       )
                                        )
        portal['folder'].invokeFactory('my315ok.policy.blog', 'blog',
                                       title="title",
                                       description=u"description",
                                       text=RichTextValue(            u"here is rich text",
                                                                       'text/plain',
                                                                       'text/html'
                                                                       )
                                        ) 

        self.browser = browser                                                             
        self.portal = portal
        
    def tearDown(self):
        pass                  
   
    def testblogfolderView(self):
        transaction.commit()
        self.browser.open(self.portal['folder'].absolute_url() + "/@@sysajax_listings")        
        self.assertTrue('@@ajaxsearch' in self.browser.contents)
    

    def testblogView(self):


        transaction.commit()        
        self.browser.open(self.portal['folder']['blog'].absolute_url() + "/@@base_view")
        self.assertTrue("here is rich text" in self.browser.contents)
