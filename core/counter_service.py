from core import db
from core.utils import set_interval

counters_to_increase=[]
interval_timeout=30

def start_cpunter_service():
    set_interval(update_counters, interval_timeout)

def increase_counter(link):
    link.counter = link.counter + 1
    db.session.commit()

def update_counters():
    while (len(counters_to_increase)):
        increase_counter(counters_to_increase.pop())