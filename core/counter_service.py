from flask import redirect
from core import db
from core.utils import set_interval
from core.models import ShortUrls

counters_to_increase=[]
interval_timeout=5
def start_counter_service():
    set_interval(update_counters, interval_timeout)

def increase_counter(short_id):
    link = ShortUrls.query.filter_by(short_id=short_id).first()
    link.counter = link.counter + 1
    db.session.commit()

def update_counters():
    while (len(counters_to_increase)):
        increase_counter(counters_to_increase.pop())

def trigger_increase_counter(link):
    counters_to_increase.append(link.short_id)
    return redirect(link.original_url)
