# -*- coding: utf-8 -*-
from PySide2 import QtWidgets
from PySide2.QtCore import QDir, Qt, QAbstractTableModel
from PySide2.QtGui import QColor, QPixmap
from elFrosher.my_modules import config_frosher
from os.path import normpath, join, dirname


class ServerTreeModel(QtWidgets.QFileSystemModel):

    def __init__(self):
        super(ServerTreeModel, self).__init__()
        self.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot)
        self._itemsdata = None
        self._root_project = None
        curentdir = dirname(__file__).split('models')[0]
        # normpath(join(curentdir, 'icons', ''))
        self.server_root = config_frosher.SERVER.replace('\\', '/')
        self.folder_server = QPixmap(normpath(join(curentdir, 'icons', 'ico_folder_srv.png')))
        self.folder_local = QPixmap(normpath(join(curentdir, 'icons', 'ico_folder_local.png')))
        self.file_server = QPixmap(normpath(join(curentdir, 'icons', 'ico_file_srv.png')))
        self.file_local = QPixmap(normpath(join(curentdir, 'icons', 'ico_file.png')))
        self.file_lock = QPixmap(normpath(join(curentdir, 'icons', 'lock.png')))
        self.file_lock_red = QPixmap(normpath(join(curentdir, 'icons', 'lock_red.png')))
        self.ico01 = QPixmap(normpath(join(curentdir, 'icons', 'lock.png')))
        self.ico02 = QPixmap(normpath(join(curentdir, 'icons', 'lock_red.png')))
        self.ico03 = QPixmap(normpath(join(curentdir, 'icons', 'ico_file.png')))
        self.ico04 = QPixmap(normpath(join(curentdir, 'icons', 'file_checked.png')))
        # 225,223,220
        self.file_sync = QColor().fromRgb(125, 223, 125)
        self.file_not_sync = QColor().fromRgb(60, 55, 62)
        self.file_old = QColor().fromRgb(185, 190, 45)
        self.file_in_work = QColor().fromRgb(225, 130, 130)
        self.file_in_work_other = QColor().fromRgb(128, 130, 225)

    def setpath(self, path):
        _idx = self.setRootPath(path)
        print('setting path: ', path)

    def update(self, items_data, root_path):
        self.beginResetModel()
        # print(u'получил словарь >> ', items_data)
        self._itemsdata = items_data
        self._root_project = root_path
        self.endResetModel()

    def data(self, index, role):
        # формат приходящего словаря
        # dict(absoluteLocalFilePath: [version, local_version, checkout, editor, asset.id])
        if index.isValid and role == Qt.TextColorRole:
            _int = self.fileInfo(index)
            _path = self.filePath(index)
            # делаем путь индекса относительным, меняем слеши на обратные как в БД
            item = normpath(_path).lower().replace(self._root_project, '').replace('\\', '/')
            db_path = self._itemsdata.get(item)
            # print('item:\t\t{}\t\tdb_path:\t\t{}'.format(item, db_path))
            if _int.isDir():
                for a in self._itemsdata.keys():
                    if item in a:
                        # окрашиваем папки в светлозеленый цвет если они синхронизированы с сервером
                        # 225,223,220
                        return self.file_sync

            # проверка что ключ есть в словаре, если нету, значит файл есть только на локале

            if db_path:
                version, local_version, checkout, editor, _id = db_path
                if version and not local_version:
                    # print('файл только на серваке')
                    return self.file_not_sync
                elif version == local_version and not checkout:
                    return self.file_sync
                elif version > local_version:
                    # print('версия устарела')
                    return self.file_old
                elif checkout and editor == config_frosher.user:
                    # print('файл в работе')
                    return self.file_in_work
                elif checkout and editor != config_frosher.user:
                    return self.file_in_work_other
            else:
                # print('файл или папка только на локале')
                # 225,223,220
                return self.file_not_sync

        elif role == Qt.DecorationRole:
            # рисуем иконки
            _int = self.fileInfo(index)
            _path = self.filePath(index)
            # item = normpath(_path).split(self._root_project)[-1]
            item = normpath(_path).lower().replace(self._root_project, '').replace('\\', '/')

            _int, info = self.fileInfo(index), index.data()
            if _int.isDir():
                # назначаем иконки разного цвета для сервера и локала
                if self.server_root in _path.lower():
                    return self.folder_server.scaledToHeight(18, Qt.SmoothTransformation)
                else:
                    return self.folder_local.scaledToHeight(18, Qt.SmoothTransformation)
            else:
                # для файлов куча проверок
                db_path = self._itemsdata.get(item)
                # print(">>> ", item)
                if db_path:
                    version, local_version, checkout, editor, _id = db_path
                    if version and not local_version:
                        # print('файл только на серваке')
                        return self.ico04.scaledToHeight(16, Qt.SmoothTransformation)
                    elif version > local_version:
                        # print('версия устарела')
                        return self.ico03.scaledToHeight(16, Qt.SmoothTransformation)
                    elif checkout and editor == config_frosher.user:
                        # print('файл в работе')
                        return self.ico02.scaledToHeight(16, Qt.SmoothTransformation)
                    elif checkout and editor != config_frosher.user:
                        # print('файл в работе')
                        return self.ico01.scaledToHeight(16, Qt.SmoothTransformation)

                # else:
                #     return self.ico04.scaledToHeight(16, Qt.SmoothTransformation)

                return self.file_server.scaledToHeight(16, Qt.SmoothTransformation)


        else:
            return super(ServerTreeModel, self).data(index, role)


class TmpTree(QtWidgets.QFileSystemModel):
    _BASE_ROLE = Qt.UserRole + 32
    LocalVersionRole = _BASE_ROLE + 1
    LastRevisionRole = _BASE_ROLE + 2
    StatusRole = _BASE_ROLE + 2

    def __init__(self, parent=None):
        super(TmpTree, self).__init__(parent)
        self.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot)
        self._itemsdata = None

    def setpath(self, path):
        _idx = self.setRootPath(path)

    def update(self, items_data):
        # print('получил слоуариг: ', items_data)
        self._itemsdata = items_data

    def add_item(self, icon, name, path):
        pass

    def condition(self, index, my_object, sec_obj):
        _path = self.filePath(index)
        db_path = self._itemsdata.get(_path) or None
        if db_path:
            if int(db_path[0]) > int(db_path[1]):
                return my_object
            else:
                return sec_obj

    def data(self, index, role):
        # формат приходящего словаря
        # dict(absoluteLocalFilePath: [version, local_version, checkout, editor, asset.id])
        if index.isValid() and role == Qt.TextColorRole:
            # _ind = self.fileInfo(index)
            _path = self.filePath(index)
            db_path = self._itemsdata.get(_path) or None
            if db_path:
                if not db_path[1]:
                    print('нет локальной версии db_path[1]')
                    return QColor().fromRgb(235, 50, 150)
                elif int(db_path[0]) > int(db_path[1]):
                    return QColor().fromRgb(50, 185, 55)
                # else:
                #     return QColor().fromRgb(15, 20, 130)
        elif role == Qt.DecorationRole:
            info = index.data()
            _ind = self.fileInfo(index)
            _path = self.filePath(index)
            db_path = self._itemsdata.get(_path) or None
            if _ind.isDir():
                if 'animation' in info:
                    ico = QPixmap('icons/002-record.png').scaledToHeight(16, Qt.SmoothTransformation)
                    return ico
                else:
                    ico = QPixmap('icons/ico_folder.png').scaledToHeight(16, Qt.SmoothTransformation)
                    return ico
            else:
                # if db_path:
                #     if not db_path[1]:
                #         print(db_path)
                #         ico = QPixmap('icons/007-frog.png').scaledToHeight(14, Qt.SmoothTransformation)
                #         return ico
                #     elif int(db_path[0]) > int(db_path[1]):
                #         ico = QPixmap('icons/005-checked.png').scaledToHeight(14, Qt.SmoothTransformation)
                #         return ico
                # todo
                ico = QPixmap('icons/ico_file.png').scaledToHeight(16, Qt.SmoothTransformation)
                return ico
        else:
            return super(TmpTree, self).data(index, role)

    # def rowCount(self, *args, **kwargs):
    #     pass
    # def roleNames(self, *args, **kwargs):
    #     result = QFileSystemModel.roleNames()
    #     result.insert(self.LocalVersionRole, 'local_version')
    #     result.insert(self.LastRevisionRole, 'last_revision')
    #     result.insert(self.StatusRole, 'status')


class DataBaseViewer(QAbstractTableModel):
    def __init__(self, datain, header):
        super(DataBaseViewer, self).__init__()
        # QAbstractTableModel.__init__(self)
        self.my_data = datain
        self.header = header

    def rowCount(self, parent):
        if self.my_data:
            x = len(self.my_data)
            return x
        else:
            return 1

    def columnCount(self, parent):
        if self.my_data:
            x = len(self.my_data[0])
            return x
        else:
            return 1
        # return super(DataBaseViewer, self).columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        return self.my_data[index.row()][index.column()]

    def setData(self, data, header):
        self.beginResetModel()
        self.my_data = data
        self.header = header
        # print('db viewer: length of data:\t', len(self.my_data))
        self.endResetModel()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)


class TableDetailsViewer(QAbstractTableModel):
    def __init__(self, datain, header):
        super(TableDetailsViewer, self).__init__()
        self.my_data = datain
        self.header = header

    def rowCount(self, parent):
        if self.my_data:
            return len(self.my_data)
        else:
            return 1

    def columnCount(self, parent):
        if self.my_data:
            # print('column count >> ', self.my_data)
            return len(self.my_data[0])
        else:
            return 1

    def data(self, index, role):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        if self.my_data:
            return self.my_data[index.row()][index.column()]
        else:
            return None

    def setData(self, data, header):
        self.beginResetModel()
        self.my_data = data
        self.header = header
        self.endResetModel()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)
