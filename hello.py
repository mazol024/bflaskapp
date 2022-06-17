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


@application.route('/home')
def home(who=' Anekdots'):
    return render_template('home.html', name=who,  salute='Hello world!')


@application.route('/news')
def news(who='Breaking News'):
    return render_template('news.html', name=who,  salute='Hello world!')


@application.route('/game1')
def games(who=' Project'):
    return render_template('games.html', name=who)


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
        files.append('\\' + f)
    return files


if __name__ == "__main__":
    application.run(host='0.0.0.0')
