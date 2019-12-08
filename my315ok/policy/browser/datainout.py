#-*- coding: UTF-8 -*-
import csv
from StringIO import StringIO
from zope import event


from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from plone.i18n.normalizer.interfaces import IUserPreferredFileNameNormalizer

from my315ok.policy.contents.blog import IBlog
from my315ok.policy.events import CreateDocEvent
from my315ok.policy import _

data_PROPERTIES = [
    'title',
#     'description',
    'text',
    'createdtime'
    ] 
# need byte string
data_VALUES = [
               u"标题".encode('utf-8'),
#                u"描述".encode('utf-8'),
               u"内容".encode('utf-8'),
               u"发布时间".encode('utf-8')
               ]


class DataInOut (BrowserView):
    """Data import and export as CSV files.
    """

    def __call__(self):
        method = self.request.get('REQUEST_METHOD', 'GET')
        if (method != 'POST') or not int(self.request.form.get('form.submitted', 0)):
            return self.index()

        if self.request.form.get('form.button.Cancel'):
            return self.request.response.redirect('%s/plone_control_panel' \
                                                  % self.context.absolute_url())

        if self.request.form.get('form.button.Import'):
            return self.importData()

        if self.request.form.get('form.button.CSVErrors'):
            return self.getCSVWithErrors()

        if self.request.form.get('form.button.Export'):
            return self.exportData()

    def getCSVTemplate(self):
        """Return a CSV template to use when importing blogs."""
        datafile = self._createCSV([])
        return self._createRequest(datafile.getvalue(), "blogs_sheet_template.csv")     

    def IdIsExist(self,Id):
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog(object_provides=IBlog.__identifier__,id=Id) 
        return bool(brains) 
            
    def importData(self):
        """Import Data from CSV file.

        In case of error, return a CSV file filled with the lines where
        errors occured.
        """
        file_upload = self.request.form.get('csv_upload', None)
        if file_upload is None or not file_upload.filename:
            return
        reader = csv.reader(file_upload)
        header = reader.next()
        if header != data_PROPERTIES:
            msg = _('Wrong specification of the CSV file. Please correct it and retry.')
            type = 'error'
            IStatusMessage(self.request).addStatusMessage(msg, type=type)
            return
        validLines = []
        invalidLines = []
        for line in reader:
            validLines.append(line)
        usersNumber = 0
        
        for line in validLines:
#            datas = dict(zip(header, line))
            datas = dict(zip(data_PROPERTIES, line))             
            try:
                name = datas['title']
                if not isinstance(name, unicode):
                    filename = unicode(name, 'utf-8')
                id = IUserPreferredFileNameNormalizer(self.request).normalize(filename)
                if self.IdIsExist(id):continue
                title = filename               
                text = datas['text']
                createdtime = datas.pop('createdtime')               
                try:
#                     pass
                    event.notify(CreateDocEvent(id,title,title,text,createdtime))
                except (AttributeError, ValueError), err:
                    logging.exception(err)
                    IStatusMessage(self.request).addStatusMessage(err, type="error")
                    return
                usersNumber += 1
            except:
                invalidLines.append(line)
                print "Invalid line: %s" % line

        if invalidLines:
            datafile = self._createCSV(invalidLines)
            self.request['csverrors'] = True
            self.request.form['blogs_sheet_errors'] = datafile.getvalue()
            msg = _('Some errors occured. Please check your CSV syntax and retry.')
            type = 'error'
        else:
            msg, type = _('Data successfully imported.'), 'info'

        IStatusMessage(self.request).addStatusMessage(msg, type=type)
        self.request['users_results'] = usersNumber
        self.request['groups_results'] = 0
        return self.index()

    def getCSVWithErrors(self):
        """Return a CSV file that contains lines witch failed."""

        users_sheet_errors = self.request.form.get('blogs_sheet_errors', None)
        if users_sheet_errors is None:
            return # XXX
        return self._createRequest(users_sheet_errors, "blogs_sheet_errors.csv")

    def exportData(self,**kw):
        """Export Data within CSV file."""

        datafile = self._createCSV(self._getDataInfos(**kw))
        return self._createRequest(datafile.getvalue(), "blogs_sheet_export.csv")

    def tranVoc(self,value):
        """ translate vocabulary value to title"""
        translation_service = getToolByName(self.context,'translation_service')
        title = translation_service.translate(
                                                  value,
                                                  domain='my315ok.policy',
                                                  mapping={},
                                                  target_language='zh_CN',
                                                  context=self.context,
                                                  default=u"未填写")
        return title 

    def _getDataInfos(self,**kw):
        """Generator filled with the blogs data."""

        catalog = getToolByName(self.context, "portal_catalog")
        query = kw
        query.update({"object_provides":IBlog.__identifier__})
        
        brains = catalog(query)
        
        for i in brains:
            dataobj = i.getObject()                                
            props = []
            if dataobj is not None:
                for p in data_PROPERTIES:
                    props.append(getattr(dataobj,p))                    
            yield props


    def _createCSV(self, lines):
        """Write header and lines within the CSV file."""
        datafile = StringIO()
        writor = csv.writer(datafile)
        writor.writerow(data_VALUES)
        map(writor.writerow, lines)
        return datafile

    def _createRequest(self, data, filename):
        """Create the request to be returned.

        Add the right header and the CSV file.
        """
        self.request.response.addHeader('Content-Disposition', "attachment; filename=%s" % filename)
        self.request.response.addHeader('Content-Type', "text/csv;charset=utf-8")
        self.request.response.addHeader("Content-Transfer-Encoding", "8bit")        
        self.request.response.addHeader('Content-Length', "%d" % len(data))
        self.request.response.addHeader('Pragma', "no-cache")
        self.request.response.addHeader('Cache-Control', "must-revalidate, post-check=0, pre-check=0, public")
        self.request.response.addHeader('Expires', "0")
        return data
