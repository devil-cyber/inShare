import pymongo
import sys
sys.path.append('../')
from __init__ import create_app
from datetime import datetime, timedelta
import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8'] 


app = create_app()
url = app.config['URL']



def connect_db():
    try:
        client = pymongo.MongoClient(url)
        print('Database connected successfully')
        return client
    except Exception as e:
        print('There is error in connecting to database: ',str(e))


def add_file(client,filename,uuid,path,size):
	db = client.file
	db = db['file_upload']
	file_meta= {'filename':filename,'uuid':uuid,
	             'path':path,'size':size,'last_updated':datetime.utcnow()}
	try:
		db.insert_one(file_meta)
		print('Data uploaded successfully')
	except  Exception as e:
		print('Error in uploading data to database: ',str(e))

    
