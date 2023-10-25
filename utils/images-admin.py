#!/usr/bin/env python
# -*- coding: utf-8 -*-

# dependencies: gspread oauth2client

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s :  %(name)s : %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.WARNING)

import os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
BASEDIR = os.path.abspath(os.path.dirname(SCRIPT_DIR))

import argparse, json, yaml

import markdown
from bs4 import BeautifulSoup

if os.path.exists(f'{SCRIPT_DIR}/names_map.tsv'):
  with open(f'{SCRIPT_DIR}/names_map.tsv', 'r') as f:
    names_map = {line.split('\t')[0]: line.split('\t')[1].strip() for line in f.readlines()}
else:
  names_map = {}
  
default_workbook = 'kent-maps'
default_worksheet = 'images'

import gspread
from gspread.cell import Cell
from oauth2client.service_account import ServiceAccountCredentials

logging.getLogger('oauth2client.client').setLevel(logging.WARNING)
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

def get_workbook(workbook=default_workbook, **kwargs):
  creds_file = f'{SCRIPT_DIR}/gcreds.json'
  creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
  client = gspread.authorize(creds)
  return client.open(workbook)

def as_hyperlink(url, label=None):
  return f'=HYPERLINK("{url}", "{label}")'

def as_image(url):
  return f'=IMAGE("{url}")'

def list_pages(base=BASEDIR):
  pages = []
  for root, _, files in os.walk(base):
    for file in files:
      if file == 'README.md':
        if ('.venv') in root: continue
        pages.append(root.replace(base, '')[1:])
  return sorted(pages)

def find_images(path):
  images = []
  md = open(path, 'r').read()
  html = markdown.markdown(md, extensions=['extra', 'toc'])
  soup = BeautifulSoup(html, 'html5lib')
  for param in soup.find_all('param'):
    image = None
    page = path.replace(f'{BASEDIR}/', '').replace('/README.md', '')
    if 've-config' in param.attrs and 'banner' in param.attrs:
      image = {'page': page, 'url': param.attrs['banner']}
    elif 've-image' in param.attrs:
      if 'url' in param.attrs:
        image = {**{'page': page}, **dict([(k, v) for k, v in param.attrs.items() if k not in ['ve-image']])}
        logger.debug(image)
      elif 'manifest' in param.attrs:
        image = {'page': page, 'manifest': param.attrs['manifest']}

    if image:
      images.append(image)
  
  return images

def transform_image_path(src_img):
  src_fname = src_img.split('/')[-1]
  if src_fname not in names_map:
    names_map[src_fname] = src_fname
  path = [pe for pe in src_img.split('/') if pe and pe != 'images'][:-1]
  return f'{"/".join(path)}/{names_map[src_fname]}'

def move_image(src, dst, image, dryrun=False, **kwargs):
  logger.info(f'{src} -> {dst}')
  if not dryrun:
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    src = src.replace(' ','\ ')
    if os.system(f'cp {src} {dst}') > 0:
      raise Exception(f'Failed to copy {src} to {dst}')
    os.remove(src)
    props = {}
    if 'label' in image: props['label'] = image['label']
    if 'description' in image: props['summary'] = image['description']
    if 'summary' in image: props['summary'] = image['summary']
    if 'license' in image: props['rights'] = image['license']
    if 'rights' in image: props['rights'] = image['rights']
    if 'attribution' in image: props['requiredStatement'] = {'label': 'attribution', 'value': image['attribution']}
    if props:
      yaml_path, _ = os.path.splitext(dst)
      yaml.dump(props, open(f'{yaml_path}.yaml', 'w'), default_flow_style=False)
  
def sync_images(essays, images, max=-1, dryrun=False, **kwargs):
  logger.info(f'sync_images: essays={essays} images={images} dryrun={dryrun}')
  names_map_updated = False
  for page in list_pages(essays):
    path = f'{essays}/{page}/README.md' if page else f'{essays}/README.md'
    md = open(path, 'r').read()
    md_updated = False
    num_updated = 0
    for img in find_images(path):
      if 'url' not in img: continue
      if img['url'].startswith('/'):
        src_img = img['url']
        src_fname = src_img.split('/')[-1]
        if src_fname not in names_map:
          names_map_updated = True
          names_map[src_fname] = src_fname
        dst_img_path = transform_image_path(src_img)
        src = f'{essays}{src_img}'
        dst = f'{images}/{dst_img_path}'
        img_url = f'https://raw.githubusercontent.com/kent-map/images/main/{dst_img_path}'
        
        if os.path.exists(src) and not os.path.exists(dst):
          logger.info(f'{src} ({os.path.exists(src)}) {dst} ({os.path.exists(dst)}) {img_url}')
          move_image(src, dst, img, dryrun=dryrun, **kwargs)
          md = md.replace(src_img, img_url)
          md_updated = True
    if md_updated:
      num_updated += 1
      if dryrun:
        print(md)
      else:
        with open(path, 'w') as f:
          f.write(md)
      if num_updated == max: break
      
  if names_map_updated:
    with open(f'{SCRIPT_DIR}/names_map.tsv', 'w') as f:
      for src, dst in names_map.items():
        f.write(f'{src}\t{dst}\n')
  
def update_google_sheets(**kwargs):
  fields = {
    'Page': 0,
    'Thumbnail': 1,
    'URL': 2
  }
  wb = get_workbook(**kwargs)
  ws = wb.worksheet(kwargs.get('worksheet', default_worksheet))
  ws_updates = []
  
  row = 0
  for page in list_pages():
    for img in find_images(page):
      if 'url' not in img: continue
      row += 1
      row_data = {
        'Page': as_hyperlink(f'https://beta.kent-maps.online/{page}', page or 'Home'),
        'URL': as_hyperlink(img['url'], img['url'].split('/')[-1]),
      }
    ws_updates += [Cell(row, fields[fld] + 1, val) for fld, val in row_data.items() if fld in fields]

  if ws_updates:
    ws_updates.sort(key=lambda cell: cell.col, reverse=False)
    ws.update_cells(ws_updates, value_input_option='USER_ENTERED')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Images admin tool')
  parser.add_argument('--debug', type=bool, default=False, action=argparse.BooleanOptionalAction, help='Generate debug output')
  parser.add_argument('--quiet', type=bool, default=False, action=argparse.BooleanOptionalAction, help='Disable logging')
  parser.add_argument('--sync', type=bool, default=False, action=argparse.BooleanOptionalAction, help='Sync images with essays')
  parser.add_argument('--max', type=int, default=-1, help='Maximum essays to process')
  parser.add_argument('--dryrun', type=bool, default=False, action=argparse.BooleanOptionalAction, help='Do dryrun')
  parser.add_argument('--essays', type=str, default=BASEDIR, help='Essays root directory')
  parser.add_argument('--images', type=str, default=os.path.abspath(f'{BASEDIR}/../images'), help='Images root directory')
  parser.add_argument('--workbook', type=str, default=default_workbook, help='Google sheets workbook')
  parser.add_argument('--worksheet', type=str, default=default_worksheet, help='Google sheets worksheet')
  args = vars(parser.parse_args())

  if args['debug']: logger.setLevel(logging.DEBUG)
  elif not args['quiet']: logger.setLevel(logging.INFO)
  args.pop('debug')
  args.pop('quiet')
    
  logger.debug(json.dumps(args, indent=2))

  if args['sync']:
    sync_images(**args)