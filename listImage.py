#!/usr/bin/python 
# 
# Script for getting a openstack image list order by owner 
# Developer: fcojperez@gmail.com
# Date: 23/09/2018 



import imp
from os import environ as env
import os
import sys
import glanceclient.v2.client as glclient 
import keystoneclient.v2_0.client as ksclient 


TABLE_HEADER = ['id','name','owner','disk_format'] 

def getGlanceCLI():
  try:
    keystone = ksclient.Client(auth_url=env['OS_AUTH_URL'],
                               username=env['OS_USERNAME'],
                               password=env['OS_PASSWORD'],
                               tenant_name=env['OS_TENANT_NAME'])
    glance_endpoint = keystone.service_catalog.url_for(service_type='image')
    return glclient.Client(glance_endpoint, token=keystone.auth_token)
  except Exception as e:
    print("Keystone file hasn't been loaded")
    print('Exception message: {}'.format(e))
    raise

def listImages(glclient):
  
  # Checking existance terminaltables module
  try:
    imp.find_module('terminaltables')
  except Exception as e:
    print('terminatables library not loaded')
    print('run: pip install terminaltables')
    print('message: {}'.format(e))
    raise

  from terminaltables import AsciiTable

  lst = sorted(map(lambda x: dict((k,v) for k,v in x.iteritems() if k in TABLE_HEADER), glclient.images.list()) , key=lambda k: k['owner'])
      
  table_data = [TABLE_HEADER] + [ [ x['id'], x['owner'], x['name'], x['disk_format']  ] for x in lst ]
  table = AsciiTable(table_data)
  print(table.table)
 

def main():
  
  try:
    glclient = getGlanceCLI()
    listImages(glclient)
  except Exception as e:
    sys.exit(1)
  
  
if __name__ == '__main__':
  main()

