from ensurepip import bootstrap
from flask import request
from flask import Flask, render_template
from datetime import datetime
from flask_bootstrap import Bootstrap
from frm1 import NameForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import glob
import requests
import os.path
from PIL import Image

application = Flask(__name__)
application.config['SECRET_KEY'] = 'Hard to guess string'
bootstrap = Bootstrap(application)


@application.route('/', methods=['GET', 'POST'])
def index():
    user_agent = request.remote_addr
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    # return f'<h2 style='color: RED'>Hello world</h2>'
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', name=name, form=form, salute='Hello world!', date1=formatted_now)


@application.route('/anekdots')
def home(who=' Anekdots'):
    return render_template('anekdots.html', name=who,  salute='Hello world!')


@application.route('/weather')
def weather():
    #code = requests.get('http://dataservice.accuweather.com/locations/v1/cities/search?apikey=BIilFHGmyYwCasU6E1me1RBkj3MNdNfN&q=Dunedin')
    code = '255042'
    myurl = 'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/' + \
        code + '?apikey=BIilFHGmyYwCasU6E1me1RBkj3MNdNfN&metric=true'
    data0 = requests.get(myurl)
    data1 = data0.json()
    print(data1)
    return render_template('weather.html', weatherdata=data1,  salute='Hello world!')


@application.route('/news')
def news():
    myurl = 'https://api.nytimes.com/svc/topstories/v2/world.json?api-key=qJzDA9Vq5xVrVG6wA7ALvNhd0AexMdv9'
    obj1 = requests.get(myurl)
    news = obj1.json()
    articles = news['results']
    return render_template('news.html', articles=articles[1:],  salute='Hello world!')


@application.route('/game1')
def games(who=' Project'):
    return render_template('games.html', name=who)


@application.route('/photofull/<path:imagepath>')
def photofull(imagepath):
    p1 = os.path.join("/", imagepath)
    return render_template('photofull.html', pic=p1)


@application.route('/budapest')
def budapest(descript='Photos from Budapest'):
    photos = []
    photos = getpics('./static/budapest/*.jpg')

    return render_template('projects.html', name=descript, photos=photos)


@application.route('/spain')
def spain(descript='Photos from Spain '):
    photos = []
    photos = getpics('./static/spain/*.jpg')

    return render_template('projects.html', name=descript, photos=photos)


@application.route('/paris')
def paris(descript='Photos from Paris'):
    photos = []
    photos = getpics('./static/paris/*.jpg')

    return render_template('projects.html', name=descript, photos=photos)


@application.route('/lolpictures')
def lolpics(descript='Funny pictures from fishki.net'):
    photos = []
    photos = getpics('./static/*.jpg')

    return render_template('projects.html', name=descript, photos=photos)


def getpics(picsdir):
    files = []
    for f in glob.glob(picsdir):
        #files.append('/' + f)
        files.append(os.path.normpath(f))
        print('your file: ' + os.path.normpath(f))
    createthumb(files)
    return files


def createthumb(ofiles):
    if not os.path.exists(os.path.normpath('./static/static')):
        os.makedirs(os.path.normpath('./static/static'))
    for f in ofiles:
        if os.path.isfile(os.path.join('/static', f)):
            continue
        else:
            img = Image.open(f)
            img = img.resize((200, 200), Image.ANTIALIAS)
            img.save(os.path.join('./static', f), 'JPEG', quality=90)


if __name__ == "__main__":
    application.run(host='0.0.0.0')
