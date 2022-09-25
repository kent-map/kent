#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Flask app for Visual Essays site.
Dependencies: bs4 expiringdict Flask Flask-Cors html5lib PyYAML requests serverless_wsgi
'''

import logging
logging.basicConfig(format='%(asctime)s : %(filename)s : \
  %(levelname)s : %(message)s', level=logging.DEBUG)
logger = logging.getLogger()

import os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
BASEDIR = os.path.dirname(SCRIPT_DIR)
logger.info(f'SCRIPT_DIR={SCRIPT_DIR} BASEDIR={BASEDIR}')

import yaml
CONFIG = yaml.load(open(f'{SCRIPT_DIR}/config.yaml', 'r').read(), Loader=yaml.FullLoader)

from time import time as now
from flask import Flask, Response, request, send_from_directory
from flask_cors import CORS
from serverless_wsgi import handle_request
import argparse
from expiringdict import ExpiringDict
from urllib.parse import urlencode

from bs4 import BeautifulSoup

import requests
logging.getLogger('requests').setLevel(logging.WARNING)

API_ENDPOINT = 'https://api.juncture-digital.org'
PREFIX = 'kent-map/kent'   # Prefix for site content, typically Github username/repo
REF = ''                # Github ref (branch)
LOCAL_CONTENT_ROOT = None

# app = Flask(__name__)
app = Flask(__name__, static_url_path='/static', static_folder=LOCAL_CONTENT_ROOT)
CORS(app)

def handler(event, context):
  return handle_request(app, event, context)

HTML_CACHE = ExpiringDict(max_len=1000, max_age_seconds=24 * 60 * 60)
SEARCH_CACHE = ExpiringDict(max_len=1000, max_age_seconds=24 * 60 * 60)

def _add_link(soup, href, attrs=None):
  link = soup.new_tag('link')
  link.attrs = {**{'href':href}, **(attrs if attrs else {})}
  soup.head.append(link)

def _add_script(soup, src, attrs=None):
  script = soup.new_tag('script')
  script.attrs = {**{'src':src}, **(attrs if attrs else {})}
  soup.body.append(script)

def _set_favicon(soup):
  logger.info('_set_favicon')
  # Remove default favicon
  for el in soup.find_all('link', {'rel':'icon'}): el.decompose()
  # Add custom favicon
  _add_link(soup, 'https://raw.githubusercontent.com/kent-map/kent/main/images/favicon.ico', {'rel':'icon', 'type':'image/png'})

def _set_style(soup):
  # Remove default favicon
  for el in soup.find_all('link', {'rel':'stylesheet'}): el.decompose()
  # Add custom stylesheet
  # _add_link(soup, '/static/css/custom.css', {'rel': 'stylesheet'})

def _customize_response(html):
  '''Perform any post-processing of API-generated HTML.'''
  # parse API-generated HTML with BeautifulSoup
  #   https://beautiful-soup-4.readthedocs.io/en/latest/
  soup = BeautifulSoup(html, 'html5lib')
  # perform custom updates to api-generated html
  _set_favicon(soup)
  # _set_style(soup)
  return str(soup)

def _get_local_content(path):
  '''For local development and testing.'''
  if path.endswith('/'): path = path[:-1]
  _paths = [f'{LOCAL_CONTENT_ROOT}{path}.md', f'{LOCAL_CONTENT_ROOT}{path}/README.md']
  for _path in _paths:
    if os.path.exists(_path):
      return open(_path, 'r').read()
  logger.warn(f'Local content not found: path={path}')

def _get_html(path, base_url, ref=REF, **kwargs):
  logger.info(f'_get_html: path={path} base_url={base_url} ref={ref} kwargs={kwargs}')
  html = ''
  status_code = 404
  if LOCAL_CONTENT_ROOT:
    md = _get_local_content(path)
    if md: # Markdown found, convert to HTML using API
      api_url = f'{API_ENDPOINT}/html/?prefix={PREFIX}&base={base_url}'
      resp = requests.post(api_url, json={'markdown':md, 'prefix':PREFIX})
      status_code, html =  resp.status_code, resp.text if resp.status_code == 200 else ''
  else:
    api_url = f'{API_ENDPOINT}/html{path}?prefix={PREFIX}&base={base_url}'
    if ref: api_url += f'&ref={ref}'
    if api_url in HTML_CACHE and 'refresh' not in kwargs:
      html = HTML_CACHE[api_url]
      status_code = 200
    else:
      resp = requests.get(api_url )
      status_code, html =  resp.status_code, resp.text if resp.status_code == 200 else ''
      if status_code == 200:
        HTML_CACHE[api_url] = html
  if status_code == 200:
    html = _customize_response(html)
    if 'localhost' in API_ENDPOINT:
      html = html.replace('https://unpkg.com/visual-essays/dist/visual-essays','http://localhost:3333/build')
  return status_code, html

@app.route('/favicon.ico')
def favicon():
  favicon = requests.get('https://raw.githubusercontent.com/kent-map/kent/main/images/favicon.ico').content
  return Response(favicon, mimetype='image/png')

@app.route('/robots.txt')
def robots_txt():
  robots = requests.get('https://raw.githubusercontent.com/kent-map/kent/main/robots.txt').text
  return Response(robots, mimetype='text/plain')

@app.route('/sitemap.txt')
def sitemap_txt():
  sitemap = requests.get('https://raw.githubusercontent.com/kent-map/kent/main/sitemap.txt').text
  return Response(sitemap, mimetype='text/plain')

@app.route('/<path:path>')
@app.route('/<path:path>/')
@app.route('/')
def render_html(path=None):
  start = now()
  qargs = dict([(k, request.args.get(k)) for k in request.args])
  base_url = f'/{"/".join(request.base_url.split("/")[3:])}'
  if base_url != '/' and not base_url.endswith('/'): base_url += '/'
  path = f'/{path}' if path else '/'
  status, html = _get_html(path, base_url, **qargs)
  logger.debug(f'render: api_endpoint={API_ENDPOINT} base_url={base_url} \
  prefix={PREFIX} path={path} status={status} elapsed={round(now()-start, 3)}')
  return html, status

@app.route('/search')
def search():
  qargs = dict([(k, request.args.get(k)) for k in request.args])
  if 'domain' in qargs and qargs['domain'] in CONFIG['google_search']:
    args = {**CONFIG['google_search'][qargs['domain']], **dict(request.args)}
    url = f'https://www.googleapis.com/customsearch/v1?{urlencode(args)}'
    if url not in SEARCH_CACHE:
      SEARCH_CACHE[url] = requests.get(url).json()
    return SEARCH_CACHE[url]
  else:
    return [], 404

if __name__ == '__main__':
  logger.setLevel(logging.INFO)
  parser = argparse.ArgumentParser(description='Image Info')
  parser.add_argument('--port', help='Port', type=int, default=9000)
  parser.add_argument('--api', help='API Endpoint', default=API_ENDPOINT)
  parser.add_argument('--prefix', help='Content URL prefix', default=PREFIX)
  parser.add_argument('--content', help='Local content root', default=None)
  args = parser.parse_args()
  API_ENDPOINT = args.api
  PREFIX = args.prefix
  LOCAL_CONTENT_ROOT = os.path.abspath(args.content) if args.content else BASEDIR
  app.static_folder = LOCAL_CONTENT_ROOT
  print(f'\nAPI_ENDPOINT: {API_ENDPOINT}\nPREFIX: {PREFIX}\nLOCAL_CONTENT_ROOT: {LOCAL_CONTENT_ROOT}\n')
  app.run(debug=True, host='0.0.0.0', port=args.port)
