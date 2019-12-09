from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='my315ok.policy',
      version=version,
      description="A plone site policy package for Plone4",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Adam tang',
      author_email='yuejun.tang@gmail.com',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['my315ok'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'bbcode',
          'Products.CMFPlone',
          'plone.app.dexterity',
          'plone.app.contenttypes',
          'collective.monkeypatcher',
          'my315ok.products',      
                                                                       
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': ['plone.app.testing',]
      },      
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
#      setup_requires=["PasteScript"],
#      paster_plugins=["ZopeSkel"],
      )
