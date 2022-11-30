from ensurepip import bootstrap
from fnmatch import translate
from pathlib import Path
from flask import request
from flask import Flask, render_template
from datetime import datetime
from flask_bootstrap import Bootstrap
from frm1 import NameForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import certifi
from urllib.request import urlopen

import glob
import requests
import os.path
from PIL import Image
import translators as ts
import concurrent.futures
from pathlib import Path

from ast import walk
import os
import shutil
from pickletools import unicodestring1
import ebooklib
import codecs
from ebooklib import epub
from html.parser import HTMLParser
from zipfile import ZipFile


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


def transtoeng(source):
    result = ts.google(source, from_language='ru', to_language='en')
    return result


@application.route('/anekdots')
def home(who=' Anekdots'):
    # return render_template('anekdots.html', name=who,  salute='Hello world!')
    url = 'https://www.anekdot.ru/random/anekdot/'
    html = urlopen(url, context=ssl.create_default_context(
        cafile=certifi.where()))
    soup = BeautifulSoup(html, "html.parser")
    tags = soup('div')
    alltext = []
    translated = []
    totranslate = ''
    counter = 3
    resulteng = []
    for tag in tags:
        text = []
        totranslate = ''
        if tag.attrs == {'class': ['text']}:
            l = tag.contents
            for a in l:
                if str(a).startswith('<br'):
                    continue
                text.append(a)
                totranslate = totranslate + a + ' '
        if len(text) > 0:
            alltext.append([text, totranslate])
            if counter <= 0:
                break
            counter -= 1
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for i in range(0, 4):
            resulteng.append(executor.submit(transtoeng, alltext[i][1]))
    for i in range(0, 4):
        translated.append([alltext[i][0], resulteng[i].result()])
    return render_template('home.html', alltext=translated)


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
    #myurl = 'https://api.nytimes.com/svc/topstories/v2/world.json?api-key=qJzDA9Vq5xVrVG6wA7ALvNhd0AexMdv9'
    myurl = 'https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=2f388081dd7f45d78d8ff8f36dd0b29c'
    obj1 = requests.get(myurl)
    news = obj1.json()
    #articles = news['results']
    articles = news['articles']
    return render_template('news.html', articles=articles[1:],  salute='Hello world!')


@application.route('/game1')
def games(who=' Project'):
    return render_template('games.html', name=who)


@application.route('/photofull/<path:imagepath>')
def photofull(imagepath):
    p1 = imagepath[imagepath.rfind('/static'):]
    #p1 = os.path.normpath(os.path.join('./', imagepath))
    #print("Full picture: " + p1)
    return render_template('photofull.html', pic1=p1)


@application.route('/budapest')
def budapest(descript='Budapest 2012'):
    photos = []
    photos = getpics('./static/budapest/*.jpg')

    return render_template('projects.html', name=descript, photos=photos)


@application.route('/spain')
def spain(descript='Spain 2012-2013'):
    photos = []
    photos = getpics('./static/spain/*.jpg')

    return render_template('projects.html', name=descript, photos=photos)


@application.route('/paris')
def paris(descript='Paris 2015'):
    photos = []
    photos = getpics('./static/paris/*.jpg')
    return render_template('projects.html', name=descript, photos=photos)


@application.route('/lolpictures')
def lolpics(descript='Some funny pictures...'):
    photos = []
    photos = getpics('./static/*.jpg')
    photos.extend(getpics('./static/*.png'))
    return render_template('projects.html', name=descript, photos=photos)

@application.route('/books')
def books():
    set_books()
    listdirs = os.scandir('templates/ebooks/')
    flist = []
    efiles = []
    for i in listdirs:
        if i.is_dir():
            efiles = os.scandir(i)
            for b in efiles:
                if b.is_file():
                    flist.append([b.name[:-4].replace('_'," "),os.path.basename(i)])
    return render_template('books.html', books=flist)


@application.route('/<path:i>')
def toc(i):
    bookdir = 'templates/ebooks/' + str(i) + '/'
    ff = os.scandir(bookdir)
    for i in ff:
        if i.is_file():
            zipfilename = bookdir + i.name
    with ZipFile(zipfilename, 'r') as zip:
        soup = BeautifulSoup(
            zip.read('META-INF/container.xml'), features='xml')
        opf = dict(soup.find('rootfile').attrs)['full-path']

        basedir = os.path.dirname(opf)
        if basedir:
            basedir = '{0}/'.format(basedir)

        c = zip.read(opf)
        soup = BeautifulSoup(c, features='xml')
        title =  soup.find('dc:title').text
        x, ncx = {}, None
        for item in soup.find('manifest').findAll('item'):
            d = dict(item.attrs)
            x[d['id']] = '{0}{1}'.format(basedir, d['href'])
            if len(x) <= 5:
                print(x, '\n')
            if d['media-type'] == 'application/x-dtbncx+xml':
                ncx = '{0}{1}'.format(basedir, d['href'])
            elif d['id'] == 'ncxtoc':
                ncx = '{0}{1}'.format(basedir, d['href'])
        z = {}
        pp = []
        if ncx:
            # get titles from the toc
            #n = zip.read('OEBPS/html/toc.ncx')
            n = zip.read(ncx)
            soup = BeautifulSoup(n, 'lxml')
            for navpoint in soup('navpoint'):
                k = navpoint.content.get('src', None)
                # strip off any anchor text
                # k = root + basedir + k.split('#')[0]
                if k:
                    k = bookdir +'book/' + basedir+ k
                    z[k] = navpoint.navlabel.text
                    pp.append([z[k], k])
            if len(pp) <= 1:
                for li in soup.find('ol').findAll('li'):
                    k= bookdir + 'book/' + basedir + li.find('a')['href']
                    pp.append([li.text,k])
    
    return render_template('contents.html', chapters = pp, title = title)


def getpics(picsdir):
    files = []
    imgfiles = []
    for f in glob.glob(picsdir):
        # for f in sorted(Path(picsdir).iterdir(), key=os.path.getmtime):
        files.append(os.path.normpath(f))
    createthumb(files)
    for i in files:
        imgfiles.append(os.path.normpath(os.path.join('./static', i)))
    imgfiles.sort(key=os.path.getmtime, reverse=True)
    return imgfiles


def createthumb(ofiles):
    if not os.path.exists(os.path.normpath('./static/static')):
        os.makedirs(os.path.normpath('./static/static'))
    for f in ofiles:
        if os.path.isfile(os.path.join('./static', f)):
            continue
        else:
            img = Image.open(f)
            img = img.resize((180, 180), Image.ANTIALIAS)
            if f[f.lower().rfind('jpg')+1:].lower() == 'jpg':
                img.save(os.path.join('./static', f), 'JPEG', quality=90)
            else:
                img.save(os.path.join('./static', f), 'PNG')



def set_books(basedir='templates/ebooks/'):
    # check dir if new book here and unpack it
    listdirs = os.scandir(basedir)
    numlist = [0]
    flist = []
    for i in listdirs:
        if i.is_dir():
            numlist.append(int(os.path.basename(i)))
        if i.is_file():
            flist.append(i)
    maxnum = max(numlist)
    for f in flist:
        maxnum += 1
        os.makedirs(basedir+str(maxnum)+'/')
        os.rename(f, basedir+str(maxnum)+'/'+f.name)
        #shutil.move(f, basedir+str(maxnum)+'/')
        ff = os.scandir(basedir+str(maxnum)+'/')
        for i in ff:
            if i.is_file():
                with ZipFile(i, 'r') as zip:
                    zip.extractall(basedir+str(maxnum)+'/book/')
    
if __name__ == "__main__":
    application.run(host='0.0.0.0')
