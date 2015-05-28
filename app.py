from flask import (
    Flask, render_template, Blueprint
)
import urllib2
import json
import chartkick

app = Flask(__name__)


def GetApplications():
	path = 'https://marketplace.firefox.com/api/v2/stats/global/apps_added_by_package/?start=2015-01-01&end=2015-12-31&interval=week&region=tn'
	response = urllib2.urlopen(path)
	data = json.load(response)

	datahosted = []
	datapackaged = []
	dataprivileged = []

	for i,j,k in zip(data['hosted'], data['packaged'], data['privileged']):
		datahosted.append([i["date"],i['count']])
		datapackaged.append([j["date"],j['count']])
		dataprivileged.append([k["date"],k['count']])

	data = [
		{'data': datahosted, 'name':'Hosted'},
		{'data': datapackaged, 'name':'Packaged'},
		{'data': dataprivileged, 'name': 'Privileged'}
	]
	return json.dumps(data)

@app.route('/')
def home():
	dataApps = GetApplications()

	return render_template('index.html',dataApps=dataApps)


ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)