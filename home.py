from __init__ import create_app
from flask import render_template

app = create_app()



@app.route('/')
def home_route():
	return {'message':'Welcome to InShare API','author':'Manikant Kumar','website':'http://manikant.codes'}