# -*- coding: utf-8 -*-
import os
from PySide2 import QtWidgets, QtCore
from os.path import dirname, normpath, join, split, getsize
from elFrosher.my_modules import config_frosher
from shutil import copy2
import logging
log = logging.getLogger('elFrosher')


class Synchronizer(object):
    def __init__(self):
        self.project_root = normpath(config_frosher.PROJECT)
        self.server_root = normpath(config_frosher.SERVER)
        self.versions = normpath(config_frosher.VERSIONS)
        if not os.path.exists(self.server_root):
            os.makedirs(self.server_root)

    def splitter(self, this_file):
        source_file = normpath(this_file).lower()
        suffix = ''
        # print('file size: ', getsize(source_file))
        if self.server_root in source_file:
            suffix = source_file.replace(self.server_root, '')[1:]
            # print('founded server path: ', '\t', self.server_root)
        elif self.project_root in source_file:
            suffix = source_file.replace(self.project_root, '')[1:]
            # print('founded local path: ', '\t', self.project_root)
        elif '${frosh}' in source_file:
            suffix = source_file.replace('${frosh}', '')[1:]
            # print('founded DB path: ', '\t', source_file)
        else:
            print('splitter else: ', source_file, '\t', suffix, '\t', self.server_root)
        suffix, filename = split(suffix)
        converted = join('${FROSH}', suffix, filename).replace('\\', '/')
        # print(suffix, ' ', filename, ' ', converted)
        return suffix, filename, converted

    def path_corrector(self, this_file, ver=1):
        source, versions, destination = '', '', ''

        # если файл подается с переменным путем, то указываем явным образом направление с сервака на локал
        this_file = normpath(this_file.lower())
        suffix, filename, converted = self.splitter(this_file)

        if '${frosh}' in this_file or self.server_root in this_file:
            source = normpath(join(self.versions, suffix, filename, str(ver), filename))
            destination = normpath(join(self.project_root, suffix, filename))
        else:
            source = this_file
            destination = normpath(join(self.server_root, suffix, filename))
            versions = join(self.versions, suffix, filename, str(ver), filename)

        # print('\n\rsource:\t\t\t', source)
        # print('destination:\t', destination)
        # print('versions:\t\t', versions, '\n\n\r')
        # print('converted:\t\t', converted)
        return source, destination, versions

    def sync_file(self, this_file, ver):
        # todo надо навесить флаг ReadOnly на все копируемые файлы, и снимать его только когда он берется в работу
        source, destination, versions = self.path_corrector(this_file, ver)
        # print('versions <<< ', versions)
        current_path = split(destination)[0]
        # print('\n\rcopyng: ', source, 'to: >> ', current_path, '\n\r')
        log
        if not os.path.exists(current_path):
            os.makedirs(current_path)
        copy2(source, destination)
        if versions:
            # print(current_path)
            current_path = split(versions)[0]
            # print('versions ', versions, ' current_path ', current_path)
            # todo это доп защита на время тестирования, потом можно грохнуть к хуям собачьим
            if not os.path.exists(current_path):
                os.makedirs(current_path)
            copy2(source, versions)



if __name__ == '__main__':
    c = Synchronizer()
    # x = normpath(r"D:\frosh\assets\obj\butterfly_01\rig_butterfly_01.ma")
    x = r"D:/frosh/assets/approaching_storm_2k.hdr"
    # x = r'D:\\frosh\\assets\\obj\\cone\\maps\\cone_diffuse_raw.tif'
    # x = r"${FROSH}\assets\approaching_storm_2k.hdr"
    # x = normpath("${FROSH}/assets/obj/butterfly_01/rig_butterfly_01.ma")
    # file = normpath(r"${FROSH}/assets/obj/flower_001/rig_flower_001.ma")

    c.splitter(x)


