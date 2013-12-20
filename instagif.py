from flask import Flask, render_template, request
from instagram import client, subscriptions
from images2gif import writeGif
from PIL import Image
import urllib, cStringIO
import uuid

app = Flask(__name__)

CONFIG = {
	'client_id':'6b8b8320cc194b50ad1bff2a8026d167',
	'client_secret':'2c226bb025254c838ea9f2b4bb13c6e5',
	'redirect_uri':'http://127.0.0.1:5000/oauth_callback'
}
unauthenticated_api = client.InstagramAPI(**CONFIG)

photos = None
file_names = None
@app.route('/')
def index_html():
	url = unauthenticated_api.get_authorize_url()	 	

	return render_template('index.html',authorize_url=url)

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
		file_names = []
		for p in photos:
			file_names.append(cStringIO.StringIO(urllib.urlopen(p).read()))
			
		images = [Image.open(fn) for fn in file_names]
		size = (150,150)
		filename = "gifs/%s.gif" % str(uuid.uuid4())
		writeGif(filename,images,duration=0.5)
		return render_template('pickpics.html',image_list=photos)
	except Exception, e:
		print e
@app.route('/test')
def test():
	url = unauthenticated_api.get_authorize_url()	 	
	return render_template('index.html',authorize_url=url)



if __name__ == '__main__':
    app.run(debug=True)
