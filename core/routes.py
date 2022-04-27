from datetime import datetime
from core.models import ShortUrlsDbConnection
from core import app, db
from random import choice
import string
from flask import render_template, request, flash, redirect, url_for

def generate_short_id(num_of_chars: int):
    """Function to generate short_id of specified number of characters"""
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))

def shortenUrl(url: string, short_id: string):
    if isValidArgs(url, short_id):
        insertShorternUrlToDb(url, short_id)
    else:  
         redirect(url_for('index'))

def isValidArgs(url: string, short_id: string):
    if short_id and ShortUrlsDbConnection.query.filter_by(short_id=short_id).first() is not None:
        flash('Please enter different custom id!')
        return False

    if not url:
        flash('The URL is required!')
        return False
    
    return True

def insertShorternUrlToDb(url: string, short_id: string):
    if not short_id:
        short_id = generate_short_id(8)

    new_link = ShortUrlsDbConnection(
        original_url=url, short_id=short_id, created_at=datetime.now())
    db.session.add(new_link)
    db.session.commit()
    short_url = request.host_url + short_id
    return render_template('index.html', short_url=short_url)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        countSiteSubmits()
        return shortenUrl(request.form['url'], request.form['custom_id'])

    return render_template('index.html')

@app.route('/<short_id>')
def redirect_url(short_id):
    link = ShortUrlsDbConnection.query.filter_by(short_id=short_id).first()
    if link:
        return redirect(link.original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))


def countSiteSubmits(url: string, short_id: string):
    if not url:
        short_url = request.host_url + short_id
        # counter++
    db.session.add(short_url)
    db.session.commit()     

    #1 create a shorten url if is not url
    #2  add to counter
    #3  update the db




# conected to db
# counter++
# every time the site is written we need to add for counter
# Upsert short url to db and update counter


# def shouldCacheSite(url: string, short_id: string):
# #     # check if the site was caching
# #     # return bool for should Cache Site


# def doCacheSite(url: string, short_id: string):
#      #To do cache to site
