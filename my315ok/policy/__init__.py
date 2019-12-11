# -*- extra stuff goes here -*-
from zope.i18nmessageid import MessageFactory

from sqlalchemy.ext import declarative
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
InputDb = "cms.db:Input db"
ORMBase = declarative.declarative_base()
## GRANT ALL PRIVILEGES ON msdb.* TO 'MSdba'@'localhost' IDENTIFIED BY 'cms391124$DBA';
linkstr = 'mysql://MSdba:cms391124$DBA@127.0.0.1:3306/ultrax?charset=utf8'
engine = create_engine(linkstr,echo=False,pool_recycle=3600)
Scope_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine,expire_on_commit=False))
Session = Scope_session()
# Set up the i18n message factory for our package
_ = MessageFactory('my315ok.policy')  # -*- extra stuff goes here -*- 

