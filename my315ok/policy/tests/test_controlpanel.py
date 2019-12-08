import unittest
from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from my315ok.policy.testing import FUNCTIONAL_TESTING

import io
import os.path
import transaction

class TestControlPanel(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_configlet(self):
        

        transaction.commit()        
        # Open Plone's site setup
        self.browser.open("%s/plone_control_panel" % portal.absolute_url())
        
        self.assertTrue('Blog In/Out' in browser.contents)
  
    def test_inoutview(self):

        transaction.commit()
        
        page = self.portal.absolute_url() + '/@@blogsinout-controlpanel'

        self.browser.open(page)
        self.assertTrue('<input type="file" name="csv_upload" />' in self.browser.contents)
        
    def test_csv_file(self):
        
        transaction.commit()        
        page = self.portal.absolute_url() + '/@@blogsinout-controlpanel'

        self.browser.open(page)
#         import pdb
#         pdb.set_trace()

        widget = 'csv_upload'
        file_path = os.path.join(os.path.dirname(__file__), 'demo.csv')
        file_ctl = self.browser.getControl(name=widget)
        with io.FileIO(file_path, 'rb') as f:
            file_ctl.add_file(f, 'text/csv', 'demo.csv')
            self.browser.getControl('Import').click()
#         self.assertTrue(self.browser.url.endswith('@@blogsinout-controlpanel'))
#         self.assertTrue('Blog In/Out' in self.browser.contents)        
