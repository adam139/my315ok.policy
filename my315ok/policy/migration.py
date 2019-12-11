# -*- coding: utf-8 -*-
from my315ok.policy import engine
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select       
from zope import event
from Products.CMFPlone.utils import safe_unicode
from my315ok.policy.events import CreateDocEvent
       
def import_contents(context):
    "import blogs"   
    
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
            .where(blogs.c.subject !=u"").limit(size).offset(offset)
            rs = con.execute(stm)
        return rs.fetchall()
    
    recorders = query({"size":2,"offset":100})
    for j in recorders:
        id = str(j[0])
        title = safe_unicode(j[1])               
        text = safe_unicode(j[2])
        createdtime = j[3]               
        try:
            event.notify(CreateDocEvent(id,title,title,text,createdtime))
        except (AttributeError, ValueError), err:
            raise("some errors raise")
        return        

                        