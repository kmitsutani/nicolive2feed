# -*- coding: utf-8
import click
import requests
import json
import yaml
import feedgenerator
import re
from os import path
from datetime import datetime, timedelta
from urllib import quote_plus
import lxml.html
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper as Dumper


def load_config(ctx, param, confpath):
    if not confpath.startswith('/'):
       srcdir = path.dirname(path.realpath(__file__))
       confpath = path.relpath(confpath, srcdir)
    with open(confpath, 'rb') as fin:
        config = json.load(fin)
    return config



def construct_url(title, status, config):
    keywordquery = config['keywordfmt'].format(title=title)
    filterquery = config['filterfmt'].format(status=status)
    optdict = config['inrel_opts']
    optdict.update(dict(keyword=keywordquery, filter=filterquery))
    queries = list()
    for k, v in optdict.items():
        k_quoted = quote_plus(k.encode('utf-8'))
        v_quoted = quote_plus(v.encode('utf-8'))
        queries.append('{0}={1}'.format(k_quoted, v_quoted))
    querystr = '&'.join(queries)
    url = '{apibase}?{querystr}'.format(querystr=querystr, **config)
    return url


def trim_time(dtspan):
    dtstr = dtspan.strip()
    dtstr = dtstr.replace(u'\u3000', '')
    dtstr = dtstr.replace(' ', '')
    wdays = (u'\u65E5', u'\u6708', u'\u706B', u'\u6C34',
             u'\u6728', u'\u91D1', u'\u571F')
    ptn = r'(?P<date>\d{4}/\d{1,2}/\d{1,2})\([' + ''.join(wdays) + r']\)(?P<time>\d{2}:\d{2})'
    match = re.match(ptn, dtstr)
    date, time = match.group('date'), match.group('time')
    dtjststr = "{date} {time}:00".format(date=date, time=time)
    dtjst = datetime.strptime(dtjststr, '%Y/%m/%d %H:%M:%S')
    dtutc = dtjst - timedelta(hours=9)
    dtstrutc = dtutc.strftime('%a, %d %b %Y %H:%m:%S GMT')
    return dtstrutc


def dom2entries(dom):
    details = dom.xpath('//div[@class="result_list"][1]//div[@class="detail"]')
    entries = list()
    for detail in details:
        time = trim_time(detail[0].text_content())
        time = time.encode('utf-8')
        a = detail[1][0]
        title = a.get('title').strip()
        title = title.encode('utf-8')
        url = a.get('href')
        print("{0}, {1}, {2}".format(time, title, url))
        


@click.command()
@click.argument('title', type=str, nargs=1)
@click.option('--status', '-s', type=click.Choice(['reserved', 'closed']),
              required=False, default='closed', nargs=1)
@click.option('--format', '-f', type=click.Choice(['rss', 'yaml', 'json']),
              required=False, default='rss')
@click.option('--output', '-o', type=str, required=False,
              default=None, nargs=1)
@click.option('--config', '-c', type=str, callback=load_config,
              required=False, default='conf.json')
def dumpfeed(title, status, format, output, config):
    url = construct_url(title, status, config)
    r = requests.get(url)
    dom = lxml.html.fromstring(r.text)
    entries = dom2entries(dom)
    channel = dict(title=title, link=url,
                   description="RSS2.0 for {title} in live.nicovideo.jp",
                   language='ja', copyright='DWANGO Co., Ltd.')

if __name__ == '__main__':
    dumpfeed()
