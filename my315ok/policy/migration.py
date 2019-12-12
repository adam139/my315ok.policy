# -*- coding: utf-8 -*-
from my315ok.policy import engine
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select, desc       
from zope import event
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from my315ok.policy.events import CreateDocEvent
from my315ok.policy.contents.blog import IBlog
       
def import_contents(context):
    "import blogs"
    
    def IdIsExist(context,Id):
        catalog = getToolByName(context, "portal_catalog")
        brains = catalog(object_provides=IBlog.__identifier__,id=Id) 
        return bool(brains)       
    
    def query(kwargs):
        """
        mysql> select pid from plone_forum_post limit 2 offset 1;
+-----+
| pid |
+-----+
|   2 |
|   3 |
+-----+
        """
        size = kwargs['size']
        offset = kwargs['offset']
        with engine.connect() as con:
            meta = MetaData(engine)
            blogs = Table('plone_forum_post', meta, autoload=True)
            stm = select([blogs.c.pid, blogs.c.subject, blogs.c.message, blogs.c.dateline])\
            .where(blogs.c.subject !=u"").order_by(desc(blogs.c.pid)).limit(size).offset(offset)
            rs = con.execute(stm)
        return rs.fetchall()
    
    recorders = query({"size":6,"offset":0})
    for j in recorders:
        id = str(j[0])
        if IdIsExist(context,id):continue
        title = safe_unicode(j[1])               
        text = safe_unicode(j[2])
        createdtime = j[3]               
        try:
            event.notify(CreateDocEvent(id,title,title,text,createdtime))
        except:
            continue
    return        

                        