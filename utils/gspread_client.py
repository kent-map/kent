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

import argparse

default_workbook = 'kent-maps'
default_worksheet = 'pages'

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

def list_pages():
  pages = []
  for root, _, files in os.walk(BASEDIR):
    for file in files:
      if file == 'README.md':
        if ('.venv') in root: continue
        pages.append('/'.join([pe for pe in root.replace(BASEDIR,'').split('/') if pe]))
  return sorted(pages)
    
if __name__ == '__main__':
  logger.setLevel(logging.INFO)
  parser = argparse.ArgumentParser(description='Google sheets client')  
  parser.add_argument('--workbook', type=str, default=default_workbook, help='Google sheets workbook')
  parser.add_argument('--worksheet', type=str, default=default_worksheet, help='Google sheets worksheet')
  args = vars(parser.parse_args())

  wb = get_workbook(**args)
  ws = wb.worksheet(args.get('worksheet', default_worksheet))

  ws_updates = []
  fields = {
    'Page': 0
  }
  for idx, page in enumerate(list_pages()):
    row = idx + 2
    url = f'https://beta.kent-maps.online/{page}'
    row_data = {
      'Page': as_hyperlink(url, page or 'Home'),
    }
    ws_updates += [Cell(row, fields[fld] + 1, val) for fld, val in row_data.items() if fld in fields]

  if ws_updates:
    ws_updates.sort(key=lambda cell: cell.col, reverse=False)
    ws.update_cells(ws_updates, value_input_option='USER_ENTERED')

  '''
  wb = get_workbook(**args)
  logger.info(wb)
  ws = wb.worksheet(args.get('worksheet', default_worksheet))
  logger.info(ws)
  
  rows = ws.get_all_values()
  logger.info(rows)
  
  # fields = rows[0]
  # field_idx = dict([(fields[i], i) for i in range(len(fields))])
  # recs = [dict([(fields[col], row[col]) for col in range(len(row))]) for row in rows[1:]]
  '''
