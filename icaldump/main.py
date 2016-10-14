import click
import arrow
from icaldump.crawler import Crawler

SCHOOL_YEAR_START = arrow.get(2016, 10, 1)
SCHOOL_YEAR_END = arrow.get(2017, 6, 30).ceil('month')

@click.command()
@click.option('--website', prompt=True)
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def cli(website, username, password):
    """Authenticate with ecampus, crawl the planning and dump an iCal file"""
    c = Crawler(username, password, website)
    planning, ical = c.crawl(SCHOOL_YEAR_START, SCHOOL_YEAR_END)
    with open('calendar.ics', 'wb') as f:
        f.write(ical)
