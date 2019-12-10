#-*- coding: UTF-8 -*-
import json
import hmac
from hashlib import sha1 as sha
from datetime import date
from datetime import datetime
from Products.CMFCore.utils import getToolByName
from my315ok.policy.testing import FUNCTIONAL_TESTING,INTEGRATION_TESTING  

from zope.component import getUtility
from zope.interface import alsoProvides
from plone.keyring.interfaces import IKeyManager
from plone.app.textfield.value import RichTextValue
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest


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
                                       subject =["blog"],
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

    def test_blogs(self):
        request = self.layer['request']
#         alsoProvides(request, IThemeSpecific)        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'size': '10',
                        'start':'0' ,
                        'sortcolumn':'id',
                        'sortdirection':'desc',
                        'searchabletext':'',
                        'datetype':'0',
                        'tag':'blog',
                        'objid':''                                                                       
                        }
# Look up and invoke the view via traversal
        box = self.portal['folder']
        view = box.restrictedTraverse('@@ajaxsearch')
        result = view()
        import pdb
        pdb.set_trace()       
        self.assertEqual(json.loads(result)['total'],2)
