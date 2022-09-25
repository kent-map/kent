#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
BASEDIR = os.path.dirname(SCRIPT_DIR)

if __name__ == '__main__':
    
    for root, dirs, files in os.walk(BASEDIR):
        root = root.replace(BASEDIR, '')
        if root and root.split('/')[1] in ('.git', '.venv', 'archive', 'articles', 'comoponents', 'css', 'geojson', 'images', 'js', 'webapp', 'utils'): continue
        for file in files:
            if file.endswith('md'):
                file = file[:-3]
                if file == 'README':
                    print(f'https://www.kent-maps.online{root}/')
                elif file not in ('index', 'howto', 'test'):
                    print(f'https://www.kent-maps.online{root}/{file}/')
