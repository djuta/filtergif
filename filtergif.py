import urllib
import cStringIO
from flask import Flask, render_template, request, abort
from instagram import client
from images2gif import writeGif
from PIL import Image
import shortuuid
from settings import CONFIG

# initialize app
app = Flask(__name__)

# initialize api
unauth_api = client.InstagramAPI(**CONFIG)

# declare arrays for photos and file names lists
photos = None
file_names = None


@app.route('/')
def index_html():
    """
    Returns landing page for application
    """
    url = unauth_api.get_authorize_url()
    return render_template('index.html', authorize_url=url)


@app.route('/oauth_callback')
def on_callback():
    """
    Returns select images page if client is authenticated
    """
    code = request.args.get('code')
    if not code:
        return 'Missing Code'
    try:
        access_token, u_info = unauth_api.exchange_code_for_access_token(code)
        if not access_token:
            return 'error'
        api = client.InstagramAPI(access_token=access_token)
        recent_media, next = api.user_recent_media()
        photos = []
        for media in recent_media:
            photos.append(media.images['low_resolution'].url)
        return render_template('pickpics.html', image_list=photos)
    except Exception, e:
        print e


@app.route('/make_gif', methods=['GET', 'POST'])
def make_gif():
    """
    creates gif image based on selected Instagram Images
    """
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
    random_name = str(shortuuid.uuid())
    filename = "static/gifs/%s.gif" % random_name
    writeGif(filename, images, duration=float(time))
    return random_name


@app.route('/gif/<gif>')
def gif(gif):
    """
    Returns gif image page
    """
    return render_template('gif.html', image=('static/gifs/%s.gif' % gif))

if __name__ == '__main__':
    app.run(debug=True)
