# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone import api
from plone.app.dexterity.behaviors import constrains
from plone.app.textfield.value import RichTextValue
from zope.dottedname.resolve import resolve
from Products.Five.utilities.marker import mark
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone.namedfile.file import NamedImage

from logging import getLogger
logger = getLogger(__name__)

@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'qidejt.policy:uninstall',
        ]


# for image field data

def _load_image(slider):
    from plone.namedfile.file import NamedImage
    import os
    filename = os.path.join(
        os.path.dirname(__file__),
        'browser',
        'static',
        'slide_{0}.jpg'.format(slider),
    )
    return NamedImage(
        data=open(filename, 'r').read(),
        filename=u'slide_{0}.jpg'.format(slider)
    )
image1 = _load_image(1)
image2 = _load_image(2)
image3 = _load_image(3)


default = { 'i': 'portal_type',
           'o': 'plone.app.querystring.operation.string.is',
            'v': 'Document'}
query = []
defaultpath = {
                    'i': 'path',
                    'o': 'plone.app.querystring.operation.string.path',
                    'v': '/',
                }
import copy

defaultpath.update({'v':'/qidedongtai/qidexinwen'})
qidexinwen = [default,defaultpath]

zuixingonggaopath = copy.copy(defaultpath)
zuixingonggaopath.update({'v':'/qidedongtai/qidegonggao'})
zuixingonggao = [default,zuixingonggaopath]

STRUCTURE = [
    {
        'type': 'Folder',
        'title': u'关于齐德',
        'id': 'guanyuqide',
        'description': u'关于齐德',
        'layout': 'tableview'
    },
    {
        'type': 'Folder',
        'title': u'齐德动态',
        'id': 'qidedongtai',
        'description': u'齐德动态',
        'layout': 'tableview',
        'children': [
                     {
        'type': 'Folder',
        'title': u'齐德新闻',
        'id': 'qidexinwen',
        'description': u'齐德新闻',
        'layout': 'tableview',
        'children': [
                     {
         'type': 'Document',
        'title': u'齐德新闻',
        'id': 'qidexinwen2',
        'description': u'齐德新闻'
        }                    
                     ]                              
                      },
                     {
        'type': 'Folder',
        'title': u'齐德公告',
        'id': 'qidegonggao',
        'description': u'齐德公告',
        'layout': 'tableview',
        'children': [
                     {
         'type': 'Document',
        'title': u'齐德公告',
        'id': 'qidegonggao2',
        'description': u'齐德公告'
        }                    
                     ]                               
                      },                     
                     {
            'type': 'my315ok.products.productfolder',
            'title': u'图片新闻',
            'id': 'tupianxinwen',
            'description': u'图片新闻',
            'children': [
                     {                                                                                     
            'type': 'my315ok.products.product',
            'title': u'图片新闻',
            'id': 'prdt1',
            'image':image1,            
            'description': u'图片新闻'
                        } ,
                         {
            'type': 'my315ok.products.product',
            'title': u'图片新闻2',
            'id': 'prdt2',
            'image':image2,            
            'description': u'图片新闻2'
                        } ,
                         {
            'type': 'my315ok.products.product',
            'title': u'图片新闻3',
            'id': 'prdt3',
            'image':image3,            
            'description': u'图片新闻3'
                        }                                                                           
                         ]                      
                      }                                                                         
                     ]
    },             
    {
        'type': 'Folder',
        'title': u'旗下产业',
        'id': 'qixiachanye',
        'description': u'旗下产业',
        'layout': 'tableview',
            'children': [
                     {                                                                                     
            'type': 'Folder',
            'title': u'水电工程',
            'id': 'shuidiangongcheng', 
            'description': u'湘潭市水电工程有限公司',
            'children': [
                     {
         'type': 'Document',
        'title': u'公司简介',
        'id': 'gongsijianjie',
        'description': u'公司简介'
        }                         
                         ]
                        } ,
                         {
            'type': 'Folder',
            'title': u'永固建材',
            'id': 'yonggujiancai',            
            'description': u'湘潭永固建材有限公司',
            'children': [
                     {
         'type': 'Document',
        'title': u'公司简介',
        'id': 'gongsijianjie',
        'description': u'公司简介'
        }                         
                         ]            
                        } ,
                         {
            'type': 'Folder',
            'title': u'民生置业',
            'id': 'minshengzhiye',          
            'description': u'湘潭市民生置业有限公司',
            'children': [
                     {
         'type': 'Document',
        'title': u'公司简介',
        'id': 'gongsijianjie',
        'description': u'公司简介'
        }                         
                         ]            
                        },
                         {
            'type': 'Folder',
            'title': u'德佑置业',
            'id': 'deyouzhiye',          
            'description': u'湘潭市德佑置业有限公司',
            'children': [
                     {
         'type': 'Document',
        'title': u'公司简介',
        'id': 'gongsijianjie',
        'description': u'公司简介'
        }                         
                         ]            
                        }                                                                                                    
                         ]         
    },             
    {
        'type': 'Folder',
        'title': u'合作伙伴',
        'id': 'hezuohuoban',
        'description': u'合作伙伴',
        'layout': 'tableview'
   
    },              
    {
        'type': 'Folder',
        'title': u'联系齐德',
        'id': 'lianxiqide',
        'description': u'联系齐德',
        'layout': 'tableview'
 
    },              
    {
        'type': 'Folder',
        'title': u'人才招聘',
        'id': 'rencaizhaopin',
        'description': u'人才招聘',
        'layout': 'tableview'        
    },             
    {
        'type': 'Folder',
        'title': u'查询集',
        'id': 'sqls',
        'description': u'查询集',
        'children': [
                     {
                     'type':'Collection',
                     'title':u'齐德新闻',
                     'description': u'齐德新闻查询集',
                     'id':'qidexinwen',
                     'sort_on':'created',
                     'sort_reversed':True,
                     'query':qidexinwen,
                     },
                     {                     
                     'type':'Collection',
                     'title':u'最新公告',
                     'description': u'最新公告查询集',
                     'id':'zuixingonggao',
                     'sort_on':'created',
                     'sort_reversed':True,                     
                     'query':zuixingonggao,
                     }                                                                                                        
                     ]
    },                           
    {
        'type': 'Folder',
        'title': u'帮助',
        'id': 'help',
        'description': u'帮助',
        'layout': 'tableview',
    }
               
]


def isNotCurrentProfile(context):
    return context.readDataFile('policy_marker.txt') is None


def post_install(context):
    """Setuphandler for the profile 'default'
    """
#     if isNotCurrentProfile(context):
#         return
    # Do something during the installation of this package
#     return
    portal = api.portal.get()
    members = portal.get('events', None)
    if members is not None:
        api.content.delete(members)
    members = portal.get('news', None)
    if members is not None:
        api.content.delete(members)
    members = portal.get('Members', None)
    if members is not None:
       members.exclude_from_nav = True
       members.reindexObject()
  

    for item in STRUCTURE:
        _create_content(item, portal)
    
    import_article(portal)
    members = portal.get('sqls', None)
    if members is not None:
       members.exclude_from_nav = True
       members.reindexObject()
    members = portal.get('help', None)
    if members is not None:
       members.exclude_from_nav = True
       members.reindexObject()       

def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
    
def _create_content(item, container):
    new = container.get(item['id'], None)
    if not new:

        new = api.content.create(
            type=item['type'],
            container=container,
            title=item['title'],
            description=item['description'],            
            id=item['id'],
            safe_id=False)
        logger.info('Created item {}'.format(new.absolute_url()))
    
    if item.get('layout', False):
        new.setLayout(item['layout'])
    if item.get('query', False):
        new.query = item['query']
    if item.get('sort_on', False):
        new.sort_on = item['sort_on']
    if item.get('sort_reversed', False):
        new.sort_reversed = item['sort_reversed']                
    if item.get('image', False):
        new.image = item['image']               
    if item.get('markif', False):
        try:
            ifobj = resolve(item['markif'])
            mark(new,ifobj)
        except:
            pass                
    if item.get('default-page', False):
        new.setDefaultPage(item['default-page'])
    if item.get('allowed_types', False):
        _constrain(new, item['allowed_types'])
    if item.get('local_roles', False):
        for local_role in item['local_roles']:
            api.group.grant_roles(
                groupname=local_role['group'],
                roles=local_role['roles'],
                obj=new)
    if item.get('publish', False):
        api.content.transition(new, to_state=item.get('state', 'published'))
    new.reindexObject()
    # call recursively for children
    for subitem in item.get('children', []):
        _create_content(subitem, new)

    
def _constrain(context, allowed_types):
    behavior = ISelectableConstrainTypes(context)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setLocallyAllowedTypes(allowed_types)
    behavior.setImmediatelyAddableTypes(allowed_types)


article = {"id":'example','title':u'测试文档','content':u'<p>这是一个测试文档</p>'}

def _create_article(article, container):
    id = str(article['id'])

    new = container.get(id, None)
    if not new:
        new = api.content.create(
            type='Document',
            container=container,
            title=article['title'],
            text = RichTextValue(article['content']),            
            id=id,
            safe_id=False)          
        new.reindexObject()         

def import_article(portal):    
    "migrate articles to document" 

    containers = list(item['id'] for item in STRUCTURE if item['id'] not in ["sqls","help"])

    for con in containers:
        container =  portal[con]                                 
        try:
            _create_article(article,container)
        except:
            continue 