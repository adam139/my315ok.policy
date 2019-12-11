#-*- coding: UTF-8 -*-
import csv
import unittest
from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from my315ok.policy.testing import FUNCTIONAL_TESTING
from my315ok.policy.browser.datainout import data_PROPERTIES
from my315ok.policy import Session,engine
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select       
from zope import event
from Products.CMFPlone.utils import safe_unicode
from my315ok.policy.events import CreateDocEvent
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

    def importData(self,readers):
        """Import Data from CSV file.

        In case of error, return a CSV file filled with the lines where
        errors occured.
        """


        validLines = []
        invalidLines = []
        for line in readers:
            validLines.append(line)
        usersNumber = 0
        
        for line in validLines:
#            datas = dict(zip(header, line))
            datas = dict(zip(data_PROPERTIES, line))
            import pdb
            pdb.set_trace()             
            try:
                name = datas['title']
                if not isinstance(name, unicode):
                    filename = unicode(name, 'utf-8')
                id = IUserPreferredFileNameNormalizer(self.request).normalize(filename)
#                 if self.IdIsExist(id):continue
                title = filename               
                text = datas['text']
                createdtime = datas.pop('createdtime')               
                try:
#                     pass
                    event.notify(CreateDocEvent(id,title,title,text,createdtime))
                except (AttributeError, ValueError), err:
                    logging.exception(err)
                    return
                usersNumber += 1
            except:
                invalidLines.append(line)
                print "Invalid line: %s" % line

        if invalidLines:
            print "some error raise"
            return

        else:
            print 'Data successfully imported.'

       

    def test_configlet(self):
        

        transaction.commit()        
        # Open Plone's site setup
        self.browser.open("%s/plone_control_panel" % self.portal.absolute_url())
        
        self.assertTrue('Blog In/Out' in self.browser.contents)
  
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
        file_path = os.path.join(os.path.dirname(__file__), 'demo10.csv')
        file_ctl = self.browser.getControl(name=widget)
        with io.FileIO(file_path, 'rb') as f:
            file_ctl.add_file(f, 'text/csv', 'demo10.csv')
            self.browser.getControl('Import').click()
#         self.assertTrue(self.browser.url.endswith('@@blogsinout-controlpanel'))
#         self.assertTrue('Blog In/Out' in self.browser.contents) 

    def read_file(self,file):
        with open(file, 'r') as f:
            data = [row for row in csv.reader(f.read().splitlines())]
        return data

    def test_local_reader(self):
        

        file_path = os.path.join(os.path.dirname(__file__), 'demo13.csv')
#         readers = self.read_file(file_path)
        readers = csv.reader(open(file_path, 'rU'),delimiter='^',dialect=csv.excel_tab)
        self.importData(readers)

    def query(self,kwargs):
        """分页查询
        """
        size = kwargs['size']
        offset = kwargs['offset']
        with engine.connect() as con:
            meta = MetaData(engine)
            blogs = Table('plone_forum_post', meta, autoload=True)
            stm = select([blogs.c.pid, blogs.c.subject, blogs.c.message, blogs.c.dateline])\
            .where(blogs.c.subject !=u"").limit(size).offset(offset)
            rs = con.execute(stm)
        return rs.fetchall()
        
    def test_load_fromdb(self):
        
        recorders = self.query({"size":2,"offset":108})
        import pdb
        pdb.set_trace()
        for j in recorders:
            id = str(j[0])
            title = safe_unicode(j[1])               
            text = safe_unicode(j[2])
            createdtime = j[3]               
            try:
                event.notify(CreateDocEvent(id,title,title,text,createdtime))
            except (AttributeError, ValueError), err:
#                     logging.exception(err)
                raise("some errors raise")
            return
            
       
