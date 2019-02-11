# -*- coding: utf-8 -*-
from os import getenv, makedirs
from os.path import normpath, join, split, exists

# path
# try:
PROJECT = getenv('FROSH').lower()
SERVER = getenv('FROSH_SERVER').lower()

# SERVER = r'O:\Frosh\frosh_depot\project_files'.lower()

VERSIONS = join(split(SERVER)[0].lower(), 'versions')
DB_FILE = join(split(SERVER)[0], 'db', 'el_frosher.db')
ASSETS_ROOT = normpath(join(PROJECT, 'assets'))
CHARACTERS = normpath(join(ASSETS_ROOT, 'chars'))
PROPS = normpath(join(ASSETS_ROOT, 'obj'))
LOCS = normpath(join(ASSETS_ROOT, 'locs'))
# except AttributeError:
#     print('need reload config')
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
BOOKMARKS_DEFAULT = {
    'characters': CHARACTERS,
    'objects': PROPS,
    'locations': LOCS
}


