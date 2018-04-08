#/usr/bin/env python3
# _*_ coding: utf-8 _*_
import os,sys
import configparser
import json

DATABASES = []

USE_DB = {
    'name': None
}

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
conf_file = os.path.join(base_dir,"config","my.conf")

conf = configparser.RawConfigParser()
conf.read(conf_file)

datadir = conf['main']['datadir']
if datadir == "":
    datadir = os.path.join(base_dir,"data")

os.chdir(datadir)
datadir_list = os.listdir(datadir)
for dir in datadir_list:
    if os.path.isdir(dir):
        DATABASES.append(dir)

dbindexfile = os.path.join(datadir,"index.mydb")
with open(dbindexfile, 'r') as dbinfo:
    DB_INFO_INDEX = json.loads(dbinfo.read())

def usedb_auth(func):
    def wapper(*args, **kwargs):
        if USE_DB.get('name') != None:
            return func(*args, **kwargs)
        else:
            print("ERROR: No database selected")
    return wapper

