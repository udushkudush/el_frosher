import pyside2uic as pui
from os.path import normpath, dirname, join


files = {'main_window': 'main_layout_v2a.ui',
         'submit_form': 'submit_form_v2.ui',
         'create_asset_form': 'create_asset_form.ui'}
folder = dirname(__file__)
for f in files:
    obj = normpath(join(folder, files.get(f)))
    out = normpath('{}.py'.format(join(folder, f)))
    pyfile = open(out, 'w')
    # print(obj, ' ', out)
    pui.compileUi(obj, pyfile)
