import os
from os.path import join, split, dirname, normpath
from shutil import copy2, rmtree


maya_custom_prefs = normpath(r'C:\Autodesk\maya\2018\python\elFrosher')
el_tuchkus = normpath(r'O:\Frosh\frosh_depot\elFrosher')

el_lokalikus = normpath(split(dirname(__file__))[0])

deploy = [
    'models/__init__.py',
    'models/models.py',
    'my_modules/__init__.py',
    'my_modules/asset_creator.py',
    'my_modules/config_frosher.py',
    'my_modules/DataBaseWorker.py',
    'my_modules/el_logger.py',
    'my_modules/synchro.py',
    'UI/__init__.py',
    'UI/converter.py',
    'UI/create_asset_form.py',
    'UI/logon_ui.py',
    'UI/main_window.py',
    'UI/style.qss',
    'UI/submit_form.py',
    '__init__.py',
    'app.py',
    'launch_shell_button.py']


def obdade_on_tuchkus():
    if os.path.exists(el_tuchkus):
        rmtree(el_tuchkus)

    for d in deploy:
        _dstn = normpath(join(el_tuchkus, d))
        if not os.path.exists(split(_dstn)[0]):
            os.makedirs(split(_dstn)[0])
        _src = normpath(join(el_lokalikus, d))
        copy2(_src, _dstn)
    copy_icons(el_lokalikus, el_tuchkus)


def copy_icons(src, dstn):
    _dstn = normpath(join(dstn, 'icons'))
    _src = normpath(join(src, 'icons'))
    if not os.path.exists(_dstn):
        os.makedirs(_dstn)
    for f in os.listdir(_src):
        if f.endswith('py') or f.endswith('png'):
            x = normpath(join(_src, f))
            copy2(x, _dstn)


def obdade_on_lokalikus():
    if os.path.exists(maya_custom_prefs):
        rmtree(maya_custom_prefs)

    for d in deploy:
        _dstn = normpath(join(maya_custom_prefs, d))
        if not os.path.exists(split(_dstn)[0]):
            os.makedirs(split(_dstn)[0])
        _src = normpath(join(el_tuchkus, d))
        copy2(_src, _dstn)

    copy_icons(el_tuchkus, maya_custom_prefs)
    print('copy from {} : to {}'.format(el_tuchkus, maya_custom_prefs))


# obdade_on_tuchkus()
obdade_on_lokalikus()
# copy_icons(el_lokalikus, el_tuchkus)
