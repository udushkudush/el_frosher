# -*- coding: utf-8 -*-
import os
from os.path import dirname, normpath, join, split
from elFrosher.my_modules import config
from shutil import copy2


class Synchronizer(object):
    def __init__(self):
        self.project_root = normpath(config.PROJECT)
        self.server_root = normpath(config.SERVER)
        self.versions = normpath(config.VERSIONS)
        if not os.path.exists(self.server_root):
            os.makedirs(self.server_root)

    def splitter(self, this_file):
        this_file = normpath(this_file).lower()
        suffix = ''
        if self.server_root in this_file:
            suffix = this_file.replace(self.server_root, '')[1:]
            print('founded server path: ', '\t', self.server_root)
        elif self.project_root in this_file:
            suffix = this_file.replace(self.project_root, '')[1:]
            print('founded local path: ', '\t', self.project_root)
        elif '${FROSH}' in this_file:
            suffix = this_file.replace('${FROSH}', '')[1:]
            print('founded DB path: ', '\t', this_file)
        else:
            print('this file : ', this_file, '\t', self.project_root, '\t', self.server_root)
        suffix, filename = split(suffix)
        converted = join('${FROSH}', suffix, filename).replace('\\', '/')
        print(suffix, '\t', filename, '\t', converted)
        return suffix, filename, converted

    def path_corrector(self, this_file, ver=1):

        source, versions = '', ''
        # если файл подается с переменным путем, значит меняем направлением с сервака на локал
        suffix, filename, converted = self.splitter(this_file)
        if '${FROSH}' in this_file:
            source = normpath(join(self.versions, suffix, filename, str(ver), filename))
            destination = normpath(join(self.project_root, suffix, filename))
        else:
            source = this_file
            destination = normpath(join(self.server_root, suffix, filename))
            versions = normpath(join(destination.replace('server', 'version'), str(ver), filename))

        print('\n\rsource:\t\t\t', source)
        print('destination:\t', destination)
        print('converted:\t\t', converted)
        print('versions:\t\t', versions, '\n\n\r')
        return source, destination, versions

    def sync_file(self, this_file, ver):
        # todo надо навесить флаг ReadOnly на все копируемые файлы, и снимать его только когда он берется в работу
        source, destination, versions = self.path_corrector(this_file, ver)
        # print('versions <<< ', versions)
        current_path = split(destination)[0]
        print('copyng: ', source, 'to: >> ', current_path, '\n\r')
        if not os.path.exists(current_path):
            os.makedirs(current_path)
        copy2(source, destination)
        if versions:
            current_path = split(versions)[0]
            # todo это доп защита на время тестирования, потом можно грохнуть к хуям собачьим
            if not os.path.exists(current_path):
                os.makedirs(current_path)
            copy2(source, versions)


if __name__ == '__main__':
    c = Synchronizer()
    x = normpath(r"D:\frosh\assets\obj\butterfly_01\rig_butterfly_01.ma")

    # x = normpath(r"D:\tmp_server\assets\obj\butterfly_01\rig_butterfly_01.ma")
    # x = normpath("${FROSH}/assets/obj/butterfly_01/rig_butterfly_01.ma")
    # file = normpath(r"${FROSH}/assets/obj/flower_001/rig_flower_001.ma")
    c.splitter(x)
