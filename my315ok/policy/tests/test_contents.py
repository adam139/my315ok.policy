import unittest
from plone.app.textfield.value import RichTextValue
from my315ok.policy.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles
#from plone.namedfile.file import NamedImage

class Allcontents(unittest.TestCase):
    layer = INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
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

        self.portal = portal
    
    def test_item_types(self):

      
        self.assertEqual(self.portal['folder'].id,'folder')             
        self.assertEqual(self.portal['folder']['doc'].id,'doc')

                                     
                  
       
        