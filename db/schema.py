from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from collections import OrderedDict


file_schema = {
	'filename':{'type':'String','required':True},
	'path':{'type':'String','required':True},
	'size':{'type':'Number','required':True},
	'uuid':{'type':'String','required':True},
	'sender':{'type':'String', 'required':False},
	'reciver':{'type':'String', 'required':False}


}