import cStringIO
import math
import urllib
from instagram import client
from images2gif import writeGif
from PIL import Image
import shortuuid
from flask import render_template, request, abort
from settings import CONFIG
from filtergif import app

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
    # get authorization url
    url = unauth_api.get_authorize_url()
    return render_template('index.html', authorize_url=url)


@app.route('/oauth_callback')
def on_callback():
    """
    Returns select images page if client is authenticated
    """
    # get oauth code
    code = request.args.get('code')
    if not code:
        abort(404)
        
    # try to get access token with code
    try:
        access_token, u_info = unauth_api.exchange_code_for_access_token(code)
        if not access_token:
            return 'error'

        # authorize api client
        api = client.InstagramAPI(access_token=access_token)

        # get users recent photos
        recent_media, next = api.user_recent_media()
        photos = []
        for media in recent_media:
            photos.append(media.images['low_resolution'].url)
        return render_template('pickpics.html', image_list=photos)

    except Exception, e:
        abort(404)


@app.route('/make_gif', methods=['GET', 'POST'])
def make_gif():
    """
    creates gif image based on selected Instagram Images
    """
    # get entered time
    time = float(request.form.get('time'))
    if time == "" and math.isnan(time):
        abort(404)

    # get array of images
    pics = request.form.getlist('pics[]')
    if not pics:
        abort(404)

    # prepare for processing
    file_names = []
    for p in pics:
        file_names.append(cStringIO.StringIO(urllib.urlopen(p).read()))

    images = [Image.open(fn) for fn in file_names]

    # generate a random filename
    random_name = str(shortuuid.uuid())
    filename = "/home/djuta/webapps/static/gifs/%s.gif" % random_name

    #generate gif sequence
    writeGif(filename, images, duration=time)
    return random_name


@app.route('/gif/<gif>')
def gif(gif):
    """
    Returns gif image page
    """
    return render_template('gif.html', image=('static/gifs/%s.gif' % gif))


@app.errorhandler(404)
def page_not_found(e):
    """
    Displays error message
    """
    return render_template('404.html'), 404
