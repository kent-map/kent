#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import root
from math import trunc
import os, sys, pygsheets

from bs4 import BeautifulSoup
import markdown as markdown_parser
from nbformat import write

# fields = ['ready', 'folder', 'essay', 'thumbnail', 'manifest', 'height', 'width', 'format', 'iiif-url', 'attribution', 'source', 'author', 'description', 'license', 'label', 'url', 'attribution-url']
# field_names_map = {'title': 'label'}
rows = []

ATTRIBUTES_IN_COLUMNS = ['attribution', 'description', 'label', 'license', 'manifest', 'title', 'url']
COLUMN_NAMES = ['Essay', 'Attribution', 'Description', 'Label', 'License', 'Manifest', 'Title', 'URL']
G_SHEET_KEY = "1I_kj9EYWFJc5iR6Pxd32hV11GO86NW1vJR58D-ZcxHA"


# If given, use given rootDir, otherwise use current directory
def getRootDir():
    if (len(sys.argv) > 1):
        return sys.argv[1]
    else:
        return '.'

# Converts 1-26 to values A-Z
def getChrFromValue(value):
    startingColumnValue = ord("A")
    return chr(startingColumnValue + value)

# Gets the last column for the given row
def getLastColumn(row):

    numColumns = len(row[0])

    # If more than 26 columns column will be 2 characters (e.g. 'AZ' or 'BH')
    if (numColumns > 26):
        firstCharValue = trunc(numColumns / 26)
        secondCharValue = numColumns - (firstCharValue * 26)

        return getChrFromValue(firstCharValue) + getChrFromValue(secondCharValue)
        
    else:
        return getChrFromValue(numColumns)


# Gets next worksheet and creates a new one if it doesn't already exist
def getWorksheet(gSheet, worksheetNum):

    try:
        worksheet = gSheet[worksheetNum]
        worksheet.clear()
    except Exception:
        gSheet.add_worksheet("Sheet{}".format(worksheetNum + 1))
        worksheet = gSheet[worksheetNum]

    return worksheet

def writeToGSheet(gSheet, rows):

    lastColumn = getLastColumn(rows[0])

    worksheetNum = 0
    worksheet = getWorksheet(gSheet, worksheetNum)

    rowNum = 1
    for i in range(len(rows)):

        row = rows[i]

        # GSheets has maximum of 1000 rows per worksheet, so start new worksheet if required
        if (rowNum > 999):
            worksheetNum += 1
            worksheet = getWorksheet(gSheet, worksheetNum)
            rowNum = 1

        cellRange = ("A{}:{}{}".format(rowNum, lastColumn, rowNum + 1))

        worksheet.update_values(cellRange, row)

        rowNum += 1

def writeToTSV(fileName, rows):

    # Clear file
    file = open(fileName, "w")
    file.write("")
    file.close()

    file = open(fileName, "a")

    for row in rows:
        rowString = ""
        for element in row[0]:
            rowString += element + "\t"
        
        file.write(rowString + "\n")

    file.close()

if __name__ == '__main__':

    rootDir = getRootDir()
    
    # Add headings to rows
    row = []
    for attr in COLUMN_NAMES:
        row.append(attr)
    rows.append([row])
    
    for dirName, subdirList, fileList in os.walk(rootDir):
    
        # For all files in sub directory
        for fname in fileList:
    
            if fname.endswith('.md'):
    
                essay = fname[:0-3]
    
                # Essay name is directory name for README.md files
                if essay == 'README':
                    essay = dirName.split('/')[-1]

                markdown = open(f'{dirName}/{fname}', 'r').read()
                markdownSoup = BeautifulSoup(markdown, 'html5lib')

                # For all <param> tags in markdown
                for tag in markdownSoup.find_all('param'):
    
                    # If tag contains ve-image attribute add image attributes to spreadsheet ????
                    if 've-image' in tag.attrs:
    
                        row = [essay]

                        for attr in ATTRIBUTES_IN_COLUMNS:

                            if attr in tag.attrs:

                                value = tag.attrs[attr]
                                value = value.replace('\t', ' ')
                                value = value.replace('\n', ' ')
                                
                                row.append(value)
                            else:
                                row.append("")

                        rows.append([row])
        
                # Don't think this code is necessary
                # html = markdown_parser.markdown(markdown, output_format='html5')
                # htmlSoup = BeautifulSoup(html, 'html5lib')
                # for tag in htmlSoup.find_all('img'):
                #     if 've-button.png' in tag.attrs['src']:                        
                #         data = {'folder': '/'.join(dirName.split('/')[1:]), 'essay': essay, 'url': tag.attrs['src']}
                #         rec = [data.get(f,'') for f in fields]

    gClient = pygsheets.authorize()
    gSheet = gClient.open_by_key(G_SHEET_KEY)
    writeToGSheet(gSheet, rows)
    
    # writeToTSV("output.tsv", rows)