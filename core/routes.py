from core.models import ShortUrls
from core import app
from flask import render_template, request, flash, redirect, url_for
from core.business_logic import shorten_url
from core.cache_service import top_ten_sites_cache, start_cache
from core.counter_service import start_counter_service,trigger_increase_counter

start_cache()
start_counter_service()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return shorten_url(request.form['url'], request.form['custom_id'])
    return render_template('index.html')


@app.route('/<short_id>')
def redirect_url(short_id):
    url_data = None
    for data in top_ten_sites_cache:
        if data.short_id == short_id:
            url_data = data
    if url_data:
        trigger_increase_counter(url_data)
        return redirect(url_data.original_url)
    else:
        link = ShortUrls.query.filter_by(short_id=short_id).first()
        if link:
            trigger_increase_counter(link)
            return redirect(link.original_url)
        else:
            flash('Invalid URL')
            return redirect(url_for('index'))
