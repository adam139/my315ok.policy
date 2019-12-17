#-*- coding: UTF-8 -*-
from plone import api
from z3c.form import field
import json
from zope.event import notify
from Acquisition import aq_inner
from Acquisition import aq_parent
from zope.interface import Interface
from Products.Five.browser import BrowserView 
from zope.component import getMultiAdapter
from zope.component import queryUtility
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.memoize.instance import memoize
from zope.interface import Interface
# from plone.directives import dexterity
from plone.memoize.instance import memoize



class BaseView(BrowserView):
    "base view"  
    
    def __init__(self,context, request):
        # Each view instance receives context and request as construction parameters
        self.context = context
        self.request = request
#         add_resource_on_request(self.request, 'load-more')    
    
    @memoize    
    def catalog(self):
        context = aq_inner(self.context)
        pc = getToolByName(context, "portal_catalog")
        return pc
    
    @memoize    
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm    
            
    @property
    def isEditable(self):
        return self.pm().checkPermission(permissions.ManagePortal,self.context)
       
    def getobj_url(self,type):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type=type)
        if bool(brains):
            return brains[0].getURL()
        else:
            return ''
    
    def tranVoc(self,value):
        """ translate vocabulary value to title"""
        translation_service = getToolByName(self.context,'translation_service')

        title = translation_service.translate(
                                                  value,
                                                  domain='plone',
                                                  mapping={},
                                                  target_language='zh_CN',
                                                  context=self.context,
                                                  default='')
        return title
    
    def getags(self):
        "get context's subject and output"
        context = self.context
        base = context.aq_parent.absolute_url()
        sts = context.subject
        label = u"标签".encode('utf-8')
        items = ['<li class="first">%s:</li>' % label]
        for j in sts:
            item = """<li>
            <a class="btn btn-default" href='%s/@@sysajax_listings?subject=%s'>%s</a></li>""" % (base,j,j)
            items.append(item)

        return "".join(items)             
    
class BlogView(BaseView):
    "content type:blog view"

    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
    
