from datetime import datetime
from core.models import ShortUrls
from core import db
from flask import render_template, request, flash, redirect, url_for
import string
from core.utils import generate_short_id

def shorten_url(url: string, short_id: string):
    if is_valid_args(url, short_id):
        if is_shorten_url_not_exists(url, short_id):
            return insert_shortern_url_to_db(url, short_id)
    else:
        return redirect(url_for('index'))

def is_valid_args(url: string, short_id: string):
    if short_id and ShortUrls.query.filter_by(short_id=short_id).first() is not None:
        flash('Please enter different custom id!')
        return False
    if not url:
        flash('The URL is required!')
        return False
    return True

def is_shorten_url_not_exists(url: string, short_id: string):
    return ShortUrls.query.filter_by(short_id=short_id, original_url=url).first() is None

def insert_shortern_url_to_db(url: string, short_id: string):
    if not short_id:
        short_id = generate_short_id(8)
    new_link = ShortUrls(
        original_url=url, short_id=short_id, created_at=datetime.now())
    db.session.add(new_link)
    db.session.commit()
    short_url = request.host_url + short_id
    return render_template('index.html', short_url=short_url)

def get_link_by_short_id(short_id:string):
    ShortUrls.query.filter_by(short_id=short_id).first()