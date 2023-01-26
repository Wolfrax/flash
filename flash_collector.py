#!/usr/bin/python
#-*- coding: utf-8 -*-

__author__ = 'mm'


import requests
from uritemplate import expand
import datetime
from datetime import datetime, timedelta
import sys
import json
import logging
from logging import handlers
import argparse
import os
import calendar
import signal

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

http_handler = handlers.HTTPHandler('www.viltstigen.se', '/logger/log', method='POST', secure=True)
http_handler.setLevel(logging.WARNING)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
http_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(http_handler)


class Flash:
    def __init__(self, from_date=None, to_date=None):
        # Assume from_date/to_date in format '2023-01-01'
        # If to_date is None, assume today's date

        if from_date is None:
            from_date = datetime.today().strftime('%Y-%m-%d')

        if to_date is None:
            to_date = datetime.today().strftime('%Y-%m-%d')

        try:
            self.from_date = datetime.strptime(from_date, "%Y-%m-%d")
            self.to_date = datetime.strptime(to_date, "%Y-%m-%d")
        except ValueError as e:
            print(e)
            sys.exit(1)

        self.db_fn = os.path.join('static', str(self.from_date.year) + "_flash_db.json")
        try:
            with open(self.db_fn, "r") as f:
                self.db = json.load(f)
        except FileNotFoundError:
            self.db = {'max': 0, 'min': 1, 'data': []}

        self.meta_fn = os.path.join('static', 'flash_meta.json')
        try:
            with open(self.meta_fn, "r") as f:
                self.meta = json.load(f)
        except FileNotFoundError:
            self.meta = {'db_files': [self.db_fn]}

        self.stats_fn = os.path.join('static', 'flash_stats.json')
        try:
            with open(self.stats_fn, "r") as f:
                self.stats = json.load(f)
        except FileNotFoundError:
            self.stats = {'data': {}}

        self.latest_fn = os.path.join('static', 'flash_latest.json')
        self.latest = {'date': '', 'data': []}

        signal.signal(signal.SIGHUP, self.terminate)
        signal.signal(signal.SIGTERM, self.terminate)

    def _year_shift(self, now):
        # New year, save last year and reset db + file name for new year
        self.save()
        self.db_fn = os.path.join('static', str(now.year) + "_flash_db.json")
        self.db = {'max': 0, 'min': 1, 'data': []}
        if self.db_fn not in self.meta['db_files']:
            self.meta['db_files'].append(self.db_fn)

    def _stats(self, ts):
        year = str(ts.year)
        month = calendar.month_abbr[ts.month]
        if year not in self.stats['data']:
            self.stats['data'][year] = {}

        if month not in self.stats['data'][year]:
            self.stats['data'][year][month] = 1
        else:
            self.stats['data'][year][month] += 1

    def get(self):
        now = self.from_date
        while now <= self.to_date:
            if now.year > (now - timedelta(days=1)).year:
                self._year_shift(now)

            url = expand('https://opendata-download-lightning.smhi.se/api/version/latest/'
                         'year/{year}/month/{month}/day/{day}/data.json',
                         year=str(now.year),
                         month=str(now.month),
                         day=str(now.day))

            logger.info("Processing {}".format(url))

            try:
                data = requests.get(url).json()
                self.latest['date'] = str(now)
                self.latest['data'] = []

                for data_elem in data['values']:
                    data_elem['lat'] = round(data_elem['lat'], 1)
                    data_elem['lon'] = round(data_elem['lon'], 1)
                    db_elem = []
                    if self.db:
                        db_elem = list(filter(lambda db_elem: db_elem['lat'] == data_elem['lat'] and
                                                              db_elem['lon'] == data_elem['lon'], self.db['data']))

                    if db_elem:
                        db_elem[0]['count'] += 1
                        self.db['max'] = max(db_elem[0]['count'], self.db['max'])
                    else:
                        self.db['data'].append({'lat': data_elem['lat'], 'lon': data_elem['lon'], 'count': 1})

                    self.latest['data'].append({'lat': data_elem['lat'], 'lon': data_elem['lon']})

                    self._stats(now)

            except requests.exceptions.RequestException as e:
                logger.warning("Error ({})getting {}".format(e, url))

            now += timedelta(days=1)

    def save(self):
        if self.db:
            with open(self.db_fn, "w") as f:
                json.dump(self.db, f, indent=4)
                f.flush()
            with open(self.meta_fn, "w") as f:
                json.dump(self.meta, f, indent=4)
                f.flush()
            with open(self.stats_fn, "w") as f:
                json.dump(self.stats, f, indent=4)
                f.flush()
            with open(self.latest_fn, "w") as f:
                json.dump(self.latest, f, indent=4)
                f.flush()

    def terminate(self):
        logger.warning("Terminating flash collector on SIGHUP/SIGTERM")
        self.save()
        sys.exit(0)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--start", required=False, default=None, help="start date (YYYY-MM-DD)")
    ap.add_argument("-e", "--end", required=False, default=None, help="end date (YYYY-MM-DD)")
    args = vars(ap.parse_args())

    flash = Flash(from_date=args['start'], to_date=args['end'])
    flash.get()
    flash.save()
