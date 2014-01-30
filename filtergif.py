import urllib
import cStringIO
from array import array
import io
from flask import Flask, render_template, request, abort, redirect, url_for
from instagram import client, subscriptions
from images2gif import writeGif
from PIL import Image
import shortuuid
from settings import CONFIG

app = Flask(__name__)

unauthenticated_api = client.InstagramAPI(**CONFIG)

photos = None
file_names = None


# Index Page
@app.route('/')
def index_html():
	url = unauthenticated_api.get_authorize_url()	 	

	return render_template('index.html',authorize_url=url)


# Pick images page
@app.route('/oauth_callback')
def on_callback():
	code = request.args.get('code')
	if not code:
		return 'Missing Code'
	try:
		access_token, user_info = unauthenticated_api.exchange_code_for_access_token(code)
		if not access_token:
			return 'error'
		api = client.InstagramAPI(access_token=access_token)
		recent_media, next = api.user_recent_media()
		photos = []		
		for media in recent_media:
			photos.append(media.images['thumbnail'].url)
		return render_template('pickpics.html',image_list=photos)
	except Exception, e:
		print e


# Make GIF method
@app.route('/make_gif', methods=['GET','POST'])
def make_gif():
	time = request.form.get('time')
	if time == "":
		#TODO: Error Message
		abort(404)
	pics = request.form.getlist('pics[]')
	if not pics:
		#TODO: Error Message
		abort(404)
	file_names = []
	for p in pics:
		file_names.append(cStringIO.StringIO(urllib.urlopen(p).read()))

	images = [Image.open(fn) for fn in file_names]
	size = (150,150)
	random_name = str(shortuuid.uuid()) 
	filename = "static/gifs/%s.gif" % random_name
	writeGif(filename,images,duration=float(time))
	return random_name


# GIF display page
@app.route('/gif/<gif>')
def gif(gif):
	return render_template('gif.html',image=('static/gifs/%s.gif' % gif))

if __name__ == '__main__':
    app.run(debug=True)
