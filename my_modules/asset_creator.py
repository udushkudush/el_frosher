# -*- coding: utf-8 -*-
import os


class AssetCreator():
    def create_asset(self, root, structure, asset_type, name):
        path=''
        if asset_type != 'maps':
            for i in structure:
                # print('struture: ', i)
                path = os.path.normpath('{}/{}/{}/{}'.format(root, asset_type, name, i))
                self.createFolders(path)
        else:
            # todo обдумать как создавать пути к ассету "текстура"
            path = os.path.normpath('{}/{}/{}'.format(root, asset_type, name.split('_')[0]))
            # print(path)

    def createFolders(self, path):
        # print(path)
        if not os.path.exists(path):
            os.makedirs(path)

