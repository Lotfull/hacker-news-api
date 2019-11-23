from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()


@tl.job(interval=timedelta(seconds=30))
def scrap_job():
    from .scrap import scrap
    scrap()
