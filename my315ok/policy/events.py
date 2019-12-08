#-*- coding: UTF-8 -*-
from zope import interface
from zope.component import adapts
from zope.component.interfaces import ObjectEvent

from my315ok.policy.interfaces import ICreateDocEvent

class CreateDocEvent(object):
    interface.implements(ICreateDocEvent)
    
    def __init__(self,id,title,description,text,createdtime):
        """角色,级别,备注"""
        self.id = id
        self.title = title
        self.description = description
        self.text = text 
        self.createdtime = createdtime


         

       