#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import root
from math import trunc
import os, sys, pygsheets

from bs4 import BeautifulSoup
import markdown as markdown_parser
from nbformat import write

rows = []

ATTRIBUTES_IN_COLUMNS = ['attribution', 'description', 'label', 'license', 'manifest', 'title', 'url']
COLUMN_NAMES = ['Essay', 'Essay Folder', 'Attribution', 'Description', 'Label', 'License', 'Manifest', 'Title', 'URL']
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

    numColumns = len(row)

    # If more than 26 columns column will be 2 characters (e.g. 'AZ' or 'BH')
    if (numColumns > 26):
        firstCharValue = trunc(numColumns / 26)
        secondCharValue = numColumns - (firstCharValue * 26)

        return getChrFromValue(firstCharValue) + getChrFromValue(secondCharValue)
        
    else:
        return getChrFromValue(numColumns)

def writeToGSheet(gSheet, rows):
    print("Writing to gSheet")

    lastRow = len(rows)
    lastColumn = getLastColumn(rows[0])

    worksheet = gSheet.sheet1

    worksheet.clear()

    worksheet.rows = lastRow
    worksheet.cols = len(rows[0])

    cellRange = ("A1:{}{}".format(lastColumn, lastRow))

    worksheet.update_values(cellRange, rows) 

def writeToTSV(fileName, rows):
    print("Writing to TSV")

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
    rows.append(row)

    print("Scraping data")
    
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
    
                    # If tag contains ve-image attribute add image attributes to spreadsheet
                    if 've-image' in tag.attrs:
    
                        essayFolder = dirName[2:]

                        row = [essay, essayFolder]

                        for attr in ATTRIBUTES_IN_COLUMNS:

                            if attr in tag.attrs:

                                value = tag.attrs[attr]
                                value = value.replace('\t', ' ')
                                value = value.replace('\n', ' ')
                                
                                row.append(value)
                            else:
                                row.append("")

                        rows.append(row)
    
    print("Connecting to gSheet")
    gClient = pygsheets.authorize()
    gSheet = gClient.open_by_key(G_SHEET_KEY)

    writeToGSheet(gSheet, rows)
    
    writeToTSV("output.tsv", rows)