from datetime import datetime, timedelta
from db.connect import connect_db
import os
import sys


def delete_data():
	client = connect_db()
	db = client.file
	db=db['file_upload']

	past_time = datetime.utcnow() - timedelta(hours=24)

	files = db.find({'last_updated':{"$lt":past_time}})
	for f in files:
		print(f)
		try:
			os.remove(f['path'])
			query = {"uuid":f['uuid']}
			db.remove(query)
		except Exception as e:
			print(str(e))
	print('Job Done')
	sys.exit()


delete_data()
	