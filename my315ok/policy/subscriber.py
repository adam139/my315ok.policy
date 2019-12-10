#-*- coding: UTF-8 -*-
from zope.site.hooks import getSite
import datetime
import bbcode
from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import createContentInContainer
from plone.app.textfield.value import RichTextValue
from my315ok.policy.contents.blogfolder import IBlogfolder


def CreateDocEvent(event):
    """this event be fired by """
    site = getSite()     
    catalog = getToolByName(site,'portal_catalog')
    wf = getToolByName(site, 'portal_workflow')
#     return
    try:
        newest = catalog.unrestrictedSearchResults({'object_provides': IBlogfolder.__identifier__})
    except:
        return     
    if not bool(newest):
        blogfolder =createContentInContainer(site,"my315ok.policy.blogfolder",
                                             checkConstraints=False,
                                             id="blogfolder",
                                             title=u"博客")
    else:
        blogfolder = newest[0].getObject()

    wf.doActionFor(blogfolder, 'publish', comment='publish' )
    
    docid = event.id        
    try:
        item =createContentInContainer(blogfolder,"my315ok.policy.blog",checkConstraints=False,id=docid)
        item.title = event.title
        item.description = event.description
        text = event.text
#         import pdb
#         pdb.set_trace()
        if isinstance(text,str):text = text.decode("utf-8")
        html = bbcode.render_html(text)
        html = html.replace("<br />\<br />","<br />")
#         if isinstance(text,str):html = html.decode("utf-8")
        item.text = RichTextValue(html,'text/html','text/html')
        createdtime = event.createdtime
        if isinstance(createdtime,str) and '-' in createdtime:
            datearray = createdtime.split('-')
            if len(datearray) >= 3:
                val = map(int,datearray)               
                item.creation_date = datetime.date(*val)  
            else:
                item.creation_date = datetime.date.today()
        else:
            # is timestamp
            ct = datetime.datetime.fromtimestamp(int(createdtime))
            ct = ct.strftime("%Y-%m-%d, %H:%M:%S")
            item.creation_date = ct
            item.setModificationDate(ct)                           
        wf.doActionFor(item, 'publish', comment='publish')
        item.reindexObject()
        return                    
    except:
        return