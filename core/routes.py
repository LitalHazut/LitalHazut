from datetime import datetime
from sqlalchemy import true
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
        if isShortenUrlNotExists(url, short_id):
            insertShorternUrlToDb(url, short_id)

        increaseCounter(url, short_id)
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

def isShortenUrlNotExists(url: string, short_id: string):
    return ShortUrlsDbConnection.query.filter_by(short_id=short_id, url=url).first() is None

def insertShorternUrlToDb(url: string, short_id: string):
    if not short_id:
        short_id = generate_short_id(8)

    new_link = ShortUrlsDbConnection(
        original_url=url, short_id=short_id, created_at=datetime.now())
    db.session.add(new_link)
    db.session.commit()
    short_url = request.host_url + short_id
    return render_template('index.html', short_url=short_url)

def increaseCounter(url: string, short_id: string, counter: int):
    url = ShortUrlsDbConnection.query.filter_by(short_id=short_id, url=url).first()
    url.counter = counter + 1
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': 
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


# def shouldCacheSite(url: string, short_id: string):


#  return bool for should Cache Site


# def doCacheSite(url: string, short_id: string):
#      To do cache to site
