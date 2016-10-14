import arrow
import requests
from arrow import Arrow
from bs4 import BeautifulSoup
from collections import defaultdict
from icalendar import Calendar, Event, vText, vCalAddress
from hashlib import md5
import json

class Crawler(object):

    def __init__(self, username, password, root_path):
        self.username = username
        self.password = password
        self.root_path = root_path

    def _auth(self):
        req = requests.post('{}/login_form'.format(self.root_path), {
            'form.submitted': 1,
            'came_from': self.root_path,
            'js_enabled': 0,
            'cookies_enabled': None,
            'login_name': None,
            'pwd_empty': 0,
            '__ac_name': self.username,
            '__ac_password': self.password,
            'submit': 'Se connecter'
        }, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'})
        req.raise_for_status()
        if ('login_form' in req.url):
            raise Exception('Could not authenticate user {}.'.format(self.username))
        else:
            self.cookies = req.history[0].cookies
        

    def _fetch_calendar(self, date):
        req = requests.get('{}/emploi_du_temps'.format(self.root_path), {
            'date': date.format('MM/DD/YYYY')
        }, cookies=self.cookies, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'})
        req.raise_for_status()
        return req.text

    def _parse_calendar(self, calendar, week):
        bs = BeautifulSoup(calendar, 'html.parser')
        day_offset_map = {}
        planning = defaultdict(list)
        for day in bs.body.find(id='DivBody').find_all('div', class_='Jour'):
            style = day['style'][:-1]
            rules = dict(item.strip().split(':') for item in style.split(';'))
            left = int(float(rules['left'][:-1]))
            if not (100 < left < 190):
                continue
            day_text = day.find('td').text
            day_offset_map[left] = arrow.get(day_text, 'dddd D MMMM', locale='fr_FR').replace(year=week.year).isoformat()
        for case in bs.body.find(id='DivBody').select('.Case'):
            if "Pas de cours cette semaine" in case.text:
                continue
            style = case['style'][:-1]
            rules = dict(item.strip().split(':') for item in style.split(';'))
            left = int(float(rules.get('left', '0.0%')[:-1]))
            if not (100 < left < 190):
                continue
            planning[day_offset_map[left]].append({
                'name': case.find('td', class_='TCase').text.title(),
                'teacher': list(case.find('td', class_='TCProf').strings)[0].title(),
                'group': list(case.find('td', class_='TCProf').strings)[1],
                'time': case.find('td', class_='TChdeb').text,
                'room': case.find('td', class_='TCSalle').text
            })
        return planning

    def crawl(self, start, end):
        self._auth()
        planning = {}
        for r in arrow.Arrow.span_range('week', start, end):
            print('Fetching calendar for week {}'.format(r[0].format('YYYY-MM-DD')))
            calendar = self._fetch_calendar(r[0])
            planning = {**planning, **self._parse_calendar(calendar, r[0])}
        return planning, self._build_ical(planning)

    def _build_ical(self, planning):
        c = Calendar()
        for day, courses in planning.items():
            for course in courses:
                event = Event()
                start_time, end_time = course['time'].split(' - ')
                event.add('uid', md5("{course[name]}.{course[teacher]}.{course[teacher]}.{start_time}.{end_time}.{day}".format(course=course, start_time=start_time, end_time=end_time, day=day).encode('utf-8')).hexdigest())
                event.add('location', course['room'])
                event.add('summary', course['name'])
                event.add('dtstart', arrow.get(day).clone().replace(hours=int(start_time.split(':')[0]), minutes=int(start_time.split(':')[1])).datetime)
                event.add('dtend', arrow.get(day).clone().replace(hours=int(end_time.split(':')[0]), minutes=int(end_time.split(':')[1])).datetime)
                event.add('description', "Prof: {}\nGroupe: {}".format(course['teacher'], course['group']))
                c.add_component(event)
        return c.to_ical()