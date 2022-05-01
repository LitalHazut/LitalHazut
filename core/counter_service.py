from core import db
from core.utils import set_interval,counters_to_increase
from core.models import ShortUrls

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

