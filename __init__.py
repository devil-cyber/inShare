import os
from flask import Flask


def create_app(test_config=None):
	app = Flask(__name__,instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY="jdgdsvdgikiysold368fbirujjvlgkjvjr"
		)

	if test_config is None:
		app.config.from_pyfile('config.py',silent=True)
	else:
		app.config.from_mapping(test_config)

	return app



