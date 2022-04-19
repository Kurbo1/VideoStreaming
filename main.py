from array import array
from ast import While
from http import server
import flask as f
import json
import os
import random
import time
import sys
import logging
import serversetup as app
from subsections.login import login as l
from subsections.authentication import authentication
from subsections.slideshow import slideshow
from werkzeug.utils import secure_filename

# Turns off console logging to clean up data
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

server = f.Flask(__name__)
r = f.request

# 5 min expiration time
EXPIRATION_TIME = 300 # Seconds
SAVE_LOCATION = r".\static"

accountControl = l.Login()
auth = authentication.Authentication(EXPIRATION_TIME)
slideshows = slideshow.Slideshow()

#Use to copy/paste - checks if user has authorization or not to be at webpage
#if not auth.checkCookie(r.cookies.get('authentication')):
#        return f.redirect('/login')

@server.route('/login', methods = ['GET', 'POST'])
def login():
    if r.method == 'POST':
        if accountControl.check(r.form.get('username'), r.form.get('password')):
            res = server.make_response(f.redirect('/'))
            cookie = auth.getRandomString(30)
            res.set_cookie('authentication', cookie)
            auth.addCookie(cookie, accountControl.getID(r.form.get('username')))
            return res
    
    if auth.checkCookie(r.cookies.get('authentication')):
        return f.redirect('/')
    else:
        return f.render_template('form.html')

@server.route('/', methods = ['GET', 'POST'])
def index():
    if r.method == 'GET':
        if not auth.checkCookie(r.cookies.get('authentication')):
            return f.redirect('/login')
        return f.render_template('index.html', slideshows = slideshows.getSlideshows())
        

@server.route('/slideshow/<slideshow>')
def slide(slideshow):
    if not auth.checkCookie(r.cookies.get('authentication')):
            return f.redirect('/login')
    return f.render_template('manageslideshow.html', slideshow = slideshow, images = [i for i in os.listdir("./static/slideshows/"+slideshow+"/")], admin = accountControl.checkPermission(accountControl.getByID(auth.getCookie(r.cookies.get("authentication"))["accountId"])["username"]) == "admin")
    #return f.render_template('upload.html', slideshow = slideshow, images = [i for i in os.listdir("./static/slideshows/"+slideshow+"/")], admin = (accountControl.checkPermission(accountControl.getByID(auth.getCookie(r.cookies.get("authentication"))["accountId"])["username"]) == "admin"))

@server.route('/admin')
def adminPanel():
    if (auth.checkCookie(r.cookies.get('authentication'))):
        if accountControl.checkPermission(accountControl.getByID(auth.getCookie(r.cookies.get("authentication"))["accountId"])["username"]) == "admin":
            return "accepted"
    return "not permitted"

@server.route('/upload')
def up():
    return f.render_template('upload.html')

@server.route('/signout', methods = ['POST'])
def signOut():
    if (auth.checkCookie(r.cookies.get('authentication'))):
        auth.deleteCookie(r.cookies.get('authentication'))
    return f.redirect('/')

@server.route('/deleteimage', methods = ['POST'])
def deleteImage():
    if os.path.isfile(f'./static/slideshows/{r.form.get("slideshow")}/{r.form.get("image")}'):
        os.remove(f'./static/slideshows/{r.form.get("slideshow")}/{r.form.get("image")}')

    return f.redirect('/slideshow/'+r.form.get("slideshow"))

@server.route('/uploadImage', methods = ["POST"])
def uploadImage():
    file = r.files['file']
    if not file.content_type[0:5] == "image":
        return 'Invalid File Type'
    file.save(os.path.join(f'./static/slideshows/{r.form.get("slideshow")}', secure_filename(file.filename)))
    return f.redirect('/slideshow/'+r.form.get("slideshow"))

if __name__ == "__main__":
    for i in auth.getCookies():
        auth.checkCookie(i["cookie"])
    debug = False
    if debug:
        while True:
            exec(input("COMMAND: "))

    #Checks to make sure every slideshow has a folder
    for i in slideshows.getSlideshows():
        if (not os.path.isdir('./static/slideshows/' + i["name"])):
            os.mkdir('./static/slideshows/' + i["name"])

    server.run()