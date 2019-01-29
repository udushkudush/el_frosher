# -*- coding: utf-8 -*-
from os import getenv
from os.path import normpath, join

# path
PROJECT = getenv('FROSH').lower()
# PROJECT = 'D:/tmp_Borzenko'
SERVER = getenv('FROSH_SERVER').lower()
VERSIONS = SERVER.replace('server', 'version').lower()
ASSETS_ROOT = normpath(join(PROJECT, 'assets'))
CHARACTERS = normpath(join(ASSETS_ROOT, 'chars'))
PROPS = normpath(join(ASSETS_ROOT, 'obj'))
LOCS = normpath(join(ASSETS_ROOT, 'locs'))

# ---- assets types ---- #
ASSET_TYPES = {
    'character': 'chars',
    'object': 'obj',
    'texture': 'maps',
    'location': 'locs'
}
# ---- assets folder structure ---- #
ASSET_STRUCTURE = [
    'maps',
    'source',
    'data/ztl',
    'data/obj'
]
# BOOKMARKS_DEFAULT =['characters', 'objects','locations']
BOOKMARKS_DEFAULT ={
        'characters': CHARACTERS,
        'objects': PROPS,
        'locations': LOCS
}
user = 'v.borzenko'
# user = 'v.verkhozin'
# user = 'a.polomoshnov'

