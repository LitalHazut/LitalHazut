from flask import redirect
from core import db,SHOW_LOGS
from core.utils import set_interval
from core.business_logic import get_link_by_short_id

counters_to_increase = []
interval_timeout = 5


def start_counter_service():
    set_interval(update_counters, interval_timeout)


def increase_counter(short_id):
    link = get_link_by_short_id(short_id)
    link.counter = link.counter + 1
    if(SHOW_LOGS):
        print('increase Counters',link.short_id)
    db.session.commit()


def update_counters():
    if(SHOW_LOGS):
        print('Update Counters',len(counters_to_increase))
    while (len(counters_to_increase)):
        increase_counter(counters_to_increase.pop())


def trigger_increase_counter(link):
    counters_to_increase.append(link.short_id)
    return redirect(link.short_id)
