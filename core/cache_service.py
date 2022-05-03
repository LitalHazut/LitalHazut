from core.models import ShortUrls
from core import SHOW_LOGS
from core.utils import set_interval

top_ten_sites_cache=[]
interval_timeout=30

def update_cache():
    topTenSitesCache = ShortUrls.query.order_by(ShortUrls.counter.desc()).limit(10).all()
    if(SHOW_LOGS):
        print('Update cache')
        for row in topTenSitesCache:
            print(row.counter,row.short_id)      

def start_cache():  
    set_interval(update_cache, interval_timeout)
