# -*- coding: utf-8 -*-
from PySide2 import QtCore, QtWidgets, QtGui
from elFrosher.UI.main_window import Ui_MainWindow as myFuckingWindow
from elFrosher.UI.submit_form import Ui_submit_dialog as submit_dialog
from elFrosher.UI.create_asset_form import Ui_Form as create_asset_dialog
from elFrosher.UI.logon_ui import Ui_Login as login_dialog

# reload = getattr(__import__('importlib'), 'reload', reload)
try:
    from importlib import reload as reload
except ImportError:
    reload = reload

import elFrosher.my_modules.DataBaseWorker as DB_Worker
reload(DB_Worker)
from elFrosher.my_modules.DataBaseWorker import DatabaseWorker

from os.path import dirname, join, normpath, normcase, getsize, split, exists
import sys
import os
import json
from elFrosher.my_modules.el_logger import ElLogger

frosh_depot = r'O:\Frosh\frosh_depot'
log_file = normpath(join(frosh_depot, 'log_{}.txt'.format(split(os.getenv('userprofile')[-1]))))
elloger = ElLogger()
elloger.set_name('elFrosher')
elloger.set_log_file(log_file)
log = elloger.log


class FrosherFileManager(QtWidgets.QMainWindow):
    __initial_folder = dirname(__file__)
    _DATABASE = None
    asset_form, submit_form = '', ''
    directory, server = '', ''
    project_root = None
    server_root = None
    versions = None

    def __init__(self, *args):
        super(FrosherFileManager, self).__init__(*args)
        log.info('init my app...')
        log.info('local setting init...')
        self.logon_ticket = normpath(join(os.getenv('userprofile'), 'Documents', 'maya', 'el_frosher.json'))
        self.local_settings = None
        self.fileslist = []
        self.table_model = ''
        self.table_details_model = ''
        self.db = DatabaseWorker()

        # проверка тикета, если нету то создать
        self.check_ticket()
        # раздаем основные пути
        self.local_settings = self.read_local_settings()
        self.project_root = self.local_settings.get('workspace').lower()
        self.server_root = self.local_settings.get('server').lower()
        os.environ['FROSH'] = self.local_settings.get('workspace')
        os.environ['FROSH_SERVER'] = self.local_settings.get('server')
        log.info('local settings: {}'.format(self.local_settings))

        from elFrosher.my_modules import config_frosher
        import elFrosher.my_modules.synchro as synchro
        reload(synchro)
        from elFrosher.my_modules.synchro import Synchronizer
        from elFrosher.my_modules.asset_creator import AssetCreator

        # устанавливаем файл базы данных
        self.db.set_data_base(join(split(self.local_settings.get('server'))[0], 'db', 'el_frosher.db'))
        self.db.set_synchronizer()
        self.synchro = Synchronizer()
        self.db.project_root = self.project_root

        self.ico_download = QtGui.QPixmap(normpath(join(self.__initial_folder, 'icons', 'arrow_down.png')))
        self.ico_check = QtGui.QPixmap(normpath(join(self.__initial_folder, 'icons', 'check.png')))
        self.ico_increment = QtGui.QPixmap(normpath(join(self.__initial_folder, 'icons', 'incremental.png')))
        self.ico_submit = QtGui.QPixmap(normpath(join(self.__initial_folder, 'icons', 'arrow-up.png')))
        self.ico_folder = QtGui.QPixmap(normpath(join(self.__initial_folder, 'icons', 'folder.png')))

        self.ui = myFuckingWindow()
        self.ui.setupUi(self)
        self.buttons()
        self.setup_all_ui()
        self.set_main_style()
        self.setup_signals()

        self.current_sender = None

    def check_ticket(self):
        if not os.path.exists(self.logon_ticket):
            dial = LoginDialog()
            if not dial.exec_():
                sys.exit()
            # self.local_settings = self.read_local_settings()
            # log.debug('ticket created')
            # os.environ['FROSH'] = self.local_settings.get('workspace')

    def accept_logon(self):
        # ---- bookmarks defaults ---- #
        try:
            self.bookmarks = QtCore.QStringListModel()
        except AttributeError:
            self.bookmarks = QtGui.QStringListModel()

        bookmarks = []
        for i in config_frosher.BOOKMARKS_DEFAULT:
            bookmarks.append(i)
        self.bookmarks.setStringList(bookmarks)
        self.ui.bookmarks.setModel(self.bookmarks)

    def read_local_settings(self):
        with open(self.logon_ticket, 'r') as f:
            x = json.load(f)
        return x

    def buttons(self):
        self.ui.get_version.setText('')
        self.ui.get_version.setIcon(self.ico_download.scaledToHeight(32, QtCore.Qt.SmoothTransformation))
        self.ui.get_version.setIconSize(QtCore.QSize(32, 32))

        self.ui.chek_out.setText('')
        self.ui.chek_out.setIcon(self.ico_check)
        self.ui.chek_out.setIconSize(QtCore.QSize(32, 32))

        self.ui.incement.setText('')
        self.ui.incement.setIcon(self.ico_increment)
        self.ui.incement.setIconSize(QtCore.QSize(32, 32))

        self.ui.submit.setText('')
        self.ui.submit.setIcon(self.ico_submit)
        self.ui.submit.setIconSize(QtCore.QSize(32, 32))

        self.ui.create_asset.setText('')
        self.ui.create_asset.setIcon(self.ico_folder)
        self.ui.create_asset.setIconSize(QtCore.QSize(32, 32))
        self.ui.user_name.setText(self.local_settings.get('user_name'))

    def setup_all_ui(self):
        import elFrosher.models.models as models
        reload(models)
        from elFrosher.models.models import DataBaseViewer, ServerTreeModel, TableDetailsViewer

        # ---- DIALOGS ----- #
        self.submit_form = SubmitDialog(self)
        self.asset_form = CreateAssetDialog(self)
        self.submit_form.hide()
        self.asset_form.hide()
        # ---- splitters ---- #
        self.ui.horizontal_left_splitter.setSizes([75, 450])
        self.ui.vertical_splitter.setSizes([350, 300])

        # ---- TREE VIEW ----- #
        self.directory = ServerTreeModel()
        self.directory.set_user(self.local_settings.get('user_name'))
        self.directory.setpath(self.project_root)
        self.server = ServerTreeModel()
        self.server.setpath(self.server_root)
        self.server.set_user(self.local_settings.get('user_name'))

        self.updater_tree_model(self.directory, self.project_root)
        # ----- set project dir in tree view ----- #
        main_tree = self.ui.project_tree
        main_tree.setModel(self.directory)
        main_tree.setRootIndex(self.directory.index(self.project_root))
        main_tree.setColumnHidden(1, True)
        main_tree.setColumnHidden(2, True)
        main_tree.setColumnHidden(3, True)
        main_tree.setColumnWidth(0, 210)
        main_tree.setHeaderHidden(True)
        main_tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        main_tree.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        main_tree.customContextMenuRequested.connect(self.context_project_tree)

        server_tree = self.ui.server_tree
        # self.server.update(dicty, self.server_root)
        self.updater_tree_model(self.server, self.server_root)
        server_tree.setModel(self.server)
        server_tree.setRootIndex(self.server.index(self.server_root))
        server_tree.setColumnHidden(1, True)
        server_tree.setColumnHidden(2, True)
        server_tree.setColumnHidden(3, True)
        server_tree.setHeaderHidden(True)
        server_tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        server_tree.customContextMenuRequested.connect(self.context_server_tree)

        # табличко
        data, header = self.table_prepare_data()
        details = self.ui.details_table
        pending = self.ui.pending_table
        if not data:
            data = [('', 'база пустая')]
        data2 = [('', 'выбери файл в дереве слева', '', 'или в верхней таблице')]
        header2 = ['(.)(.)', '(o)', '(.)(.)', '(o)']

        self.table_model = DataBaseViewer(data, header)
        self.table_details_model = DataBaseViewer(data2, header2)

        pending.setModel(self.table_model)
        details.setModel(self.table_details_model)

        pending.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        pending.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        pending.verticalHeader().hide()
        pending.setColumnWidth(0, 36)
        pending.setColumnWidth(1, 285)
        pending.setColumnWidth(2, 135)
        pending.setColumnWidth(3, 120)
        pending.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        # pending.horizontalHeader().resizeContentPrecision(5)

        details.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        details.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        details.verticalHeader().hide()
        details.setColumnWidth(0, 36)
        # details.setColumnWidth(1, 180)
        details.resizeColumnToContents(1)
        w = details.columnWidth(1)
        details.setColumnWidth(2, 48)
        details.setColumnWidth(3, 210)
        details.setColumnWidth(4, 75)
        details.resizeColumnToContents(1)
        details.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        # details.horizontalHeader().setResizeContentsPrecision(2)
        # pending.customContextMenuRequested.connect(self.context_table)
        # self.ui.details_table.verticalHeader().setSectionSize(15)

    def setup_signals(self):
        # сигналы для деревьев
        self.ui.project_tree.selectionModel().selectionChanged.connect(self.click_project_tree)
        # self.ui.project_tree.expanded.connect(self.expander)
        self.ui.server_tree.selectionModel().selectionChanged.connect(self.click_server_tree)

        self.ui.submit.clicked.connect(self.submit_clicked)
        self.ui.get_version.clicked.connect(self.get_version_clicked)
        self.ui.create_asset.clicked.connect(self.show_asset_create)
        self.ui.chek_out.clicked.connect(self.checkout)
        # self.ui.bookmarks.clicked.connect(self.bookmark_select)

        # диалоги
        self.asset_form.dialog.close_btn.clicked.connect(lambda x: self.asset_form.hide())
        self.asset_form.dialog.create_asset_btn.clicked.connect(self.create_asset)
        self.submit_form.dialog.confirm_submit.clicked.connect(self.submit_func)
        # todo обработку выделенных файлов в дереве добавить
        # таблицы
        self.ui.pending_table.clicked.connect(self.pending)
        self.ui.details_table.customContextMenuRequested.connect(self.context_table)
        self.ui.details_table.clicked.connect(self.test)
        # self.ui.details_table.model()  #dataChanged(lambda x: print('--data is changed--'))

    def updater_tree_model(self, model, model_root):
        dicty = self.db.get_dict(self.local_settings.get('user_name'))
        model.update(dicty, model_root)

    def update_tree_views(self, view, model, model_root):
        _ind = view.currentIndex()
        self.updater_tree_model(model, model_root)
        view.setRootIndex(model.index(model_root))
        view.setCurrentIndex(_ind)

    def table_prepare_data(self, search=None):
        # выбираем таблицу main_info
        table = 'main_info'
        # если есть параметр фильтра то отсеиваем данные по входящему значению
        if search:
            # select pending, name, file from main_info where file like '%/assets/chars%'
            data = """SELECT pending, comment, author, submit_date
                FROM '{}' WHERE file LIKE '%{}%'""".format(table, search)
        else:
            data = "SELECT pending, comment, author, submit_date FROM '{}'".format(table)
        data = self.db.read_data(data, single=False)
        # очищаем список от дублирующих записей и сортируем по номеру пенд листа
        data = sorted(list(set(data)), key=lambda k: k[0])
        header = ['list', 'comment', 'author', 'date']
        return data, header

    def update_table_model(self, sender):
        self.current_sender = sender
        # забираем текущий индекс из дерева
        info = self.current_sender.model().filePath(self.current_sender.currentIndex())

        # удаляем префикс из пути файла
        __, __, search = self.synchro.splitter(info)
        data, header = self.table_prepare_data(search)
        self.table_updater(self.table_model, data, header)

    @staticmethod
    def table_updater(table_model, data, header=None):
        if data:
            table_model.setData(data, header)
        else:
            data = [('нет', 'записей', '(.)(.)')]
            table_model.setData(data, header)

    def pending(self):
        sender = self.sender()

        ' для начала получить данные из строки независимо от ячейки '
        row = sender.selectionModel().selectedRows()[0].row()

        pending_list, column_history = '', ''
        for x in range(sender.model().columnCount(sender)):
            header_item = sender.model().headerData(x, QtCore.Qt.Horizontal)
            if 'list' in header_item:
                pending_list = sender.model().index(row, int(x)).data()

        text = "SELECT asset_id, name, rev, file FROM main_info WHERE pending = '{}'".format(pending_list)
        data = self.db.read_data(text, single=False)
        header = ['id', 'file name', 'version', 'path']
        self.table_updater(self.table_details_model, data, header)

    def test(self):
        table = self.ui.details_table
        row = table.selectionModel().selectedRows()[0].row()
        column_file, column_history = '', ''
        for x in range(table.model().columnCount(table)):
            header_item = table.model().headerData(x, QtCore.Qt.Horizontal)
            if header_item == 'path':
                column_file = int(x)
            if header_item == 'version':
                column_history = int(x)
        this_file = table.model().index(row, column_file).data()
        version = table.model().index(row, column_history).data()

    def context_table(self):
        # """ контекстное меню """
        menu = QtWidgets.QMenu(self)
        menu.setObjectName('database')
        # menu.setIconSize(QtCore.QSize(16, 16))
        # todo связать с функций отката до выбранной версии
        first = menu.addAction(self.ico_download.scaledToHeight(20, QtCore.Qt.SmoothTransformation), 'get version')
        # menu.addSeparator()
        action = menu.exec_(QtGui.QCursor.pos())

        ' для начала получить данные из строки независимо от ячейки '
        table = self.ui.details_table
        row = table.selectionModel().selectedRows()[0].row()
        column_file, column_history = '', ''
        for x in range(table.model().columnCount(table)):
            header_item = table.model().headerData(x, QtCore.Qt.Horizontal)
            if header_item == 'path':
                column_file = int(x)
            if header_item == 'version':
                column_history = int(x)
        this_file = table.model().index(row, column_file).data()
        version = table.model().index(row, column_history).data()
        if action == first:
            self.get_version(this_file, version)
            self.update_table_model(self.current_sender)

    def click_project_tree(self):
        self.ui.submit.setEnabled(True)
        self.click_tree(self.ui.project_tree)

    def click_server_tree(self):
        # откулючаем кнопку сабмита, так как из дерева сервера делать это нельзя
        self.ui.submit.setEnabled(False)
        self.click_tree(self.ui.server_tree)

    def click_tree(self, sender):
        # self.current_sender = self.ui.project_tree
        self.current_sender = sender

        # а пока обновляем данные из БД
        # todo тут происходит двойной вызов, надо ограничиться текущим деревом
        _inf = self.current_sender.model().fileInfo(self.current_sender.currentIndex())
        if not _inf.isDir():
            __, __, last_file = self.synchro.splitter(_inf.filePath())
            text = "SELECT asset_id, name, history, comment, file FROM main_info WHERE file = '{}'".format(last_file)
            # забираем все записи о файле чтобы вывести всю историю изменений
            data = self.db.read_data(text, single=False)
            header = ['id', 'file name', 'version', 'comment', 'path']
            self.table_updater(self.table_details_model, data, header)
            log.info('data from db:\t{}'.format(data))
        self.update_table_model(self.current_sender)

    def context_project_tree(self):
        menu = QtWidgets.QMenu(self)
        menu.setObjectName('context_project_tree')

        ico1 = self.ico_download.scaledToHeight(20, QtCore.Qt.SmoothTransformation)
        get_latest = menu.addAction(ico1, 'get latest version')

        ico2 = self.ico_check.scaledToHeight(20, QtCore.Qt.SmoothTransformation)
        checkout = menu.addAction(ico2, 'checkout')

        ico3 = self.ico_submit.scaledToHeight(20, QtCore.Qt.SmoothTransformation)
        submit = menu.addAction(ico3, 'submit')

        action = menu.exec_(QtGui.QCursor.pos())

        if action == get_latest:
            self.get_version()
        elif action == checkout:
            self.checkout()
        elif action == submit:
            self.submit_form.show()

    def context_server_tree(self):
        menu = QtWidgets.QMenu(self)
        menu.setObjectName('context_server_tree')

        ico1 = self.ico_download.scaledToHeight(20, QtCore.Qt.SmoothTransformation)
        get_latest = menu.addAction(ico1, 'get latest version')

        action = menu.exec_(QtGui.QCursor.pos())
        sender = self.sender()
        model = sender.model()
        _ind = sender.selectionModel().selectedIndexes()
        indexes = [x for x in _ind if x.column() == 0]
        self.fileslist = [model.filePath(x) for x in indexes if not model.fileInfo(x).isDir()]

        if action == get_latest:
            self.get_version()

    def file_collector(self, sender=None):
        # обнуляем список на случай если сабмит не произошел и там сохранились старые выделенки
        self.fileslist = []
        # собираем список файлов чтобы оформить пакет для отправки в БД по умолчанию собираем из локального дерева
        xx = self.ui.trees_views.currentWidget().objectName()
        if xx == 'workspace':
            view = self.ui.project_tree
        else:
            view = self.ui.server_tree

        view = sender
        model = view.model()
        _ind = view.selectionModel().selectedIndexes()
        indexes = [x for x in _ind if x.column() == 0]
        fileslist = [normpath(model.filePath(x)) for x in indexes if not model.fileInfo(x).isDir()]
        for f in fileslist:
            log.debug('selected file:\t{}'.format(f))
        # self.current_sender = None
        return fileslist

    def submit_clicked(self):
        # self.current_sender = self.ui.project_tree
        self.fileslist = self.file_collector(self.ui.project_tree)
        self.submit_form.show()

    def get_version_clicked(self):
        # кнопка на панельке берет последнюю версию, индекс берет из того последнего юзаного дерева
        self.fileslist = self.file_collector(self.current_sender)
        self.get_version()

    def submit_func(self):
        """сабмит ебана"""
        # сабмитить можно только с локального дерева, значит выставляем его в качестве текущего сендера
        self.current_sender = self.ui.project_tree
        comment = self.submit_form.dialog.comment.toPlainText()
        print('capture comment ', comment)
        if comment:
            comment = comment
        author = self.local_settings.get('user_name')
        # собираем список файлов чтобы оформить пакет для отправки в БД
        if len(self.fileslist) > 0:
            ' отправляем сразу весь список файлов в БД '
            self.db.multiple_assets_records(self.fileslist, author, comment=comment)
            ' обновляем таблицу представления из БД '
            self.update_table_model(self.ui.project_tree)
            ' очищаем поле коментария и закрываем к хуям окошко '
            self.submit_form.dialog.comment.setPlainText('')
            self.submit_form.hide()
        else:
            print('fileslist: ', len(self.fileslist), '\n\r\r', self.fileslist)
        # обнуляем список выделеных файлов и обновляем деревья
        self.fileslist = []
        self.update_tree_views(self.ui.project_tree, self.directory, self.project_root)
        self.update_tree_views(self.ui.server_tree, self.server, self.server_root)

    def get_version(self, filename=None, ver=None):
        """нужно получить путь к файлу и номер версии который мы хотим залить на локал"""
        author = self.local_settings.get('user_name')

        """если не указан файл значит юзер сделал запрос из дерева, тогда просто вызываем файлколлектор
            и обновляем список выбранных ассетов до последних версий"""
        if not filename and not ver:
            for f in self.fileslist:
                # конвертируем путь
                __, __, f = self.synchro.splitter(f)

                f = f.replace('\\', '/')
                # забираем из БД самую последнюю версию файла
                request_data = "SELECT version FROM assets WHERE assets.file='{}'".format(f)
                ver = self.db.read_data(request_data)[0]

                log.debug('geting file: {}\t version: {}'.format(f, ver))
                self.db.get_version(f, author, ver)
            # обнуляем список выбранных файлов
            self.fileslist = []
        elif filename and ver:
            # из таблицы можно выбрать только одну версию
            self.db.get_version(filename, author, ver)

        # обновляем деревья
        self.update_tree_views(self.ui.project_tree, self.directory, self.project_root)
        self.update_tree_views(self.ui.server_tree, self.server, self.server_root)

    def checkout(self):
        # " функция почемает файл в работу "
        # и отправляем в датабэйзера список файлов и сразу обнуляем его
        xx = self.ui.trees_views.currentWidget().objectName()
        if xx == 'workspace':
            self.current_sender = self.ui.project_tree
            print('localik')
        else:
            self.current_sender = self.ui.server_tree
            print('servachok')

        self.fileslist = self.file_collector(self.current_sender)
        self.db.change_status(self.fileslist, self.local_settings.get('user_name'))
        self.fileslist = []

        self.update_tree_views(self.ui.project_tree, self.directory, self.project_root)
        self.update_tree_views(self.ui.server_tree, self.server, self.server_root)

    def show_asset_create(self):
        self.asset_form.asset_type_cb.clear()
        for i in config_frosher.ASSET_TYPES:
            self.asset_form.asset_type_cb.addItem(i)
        self.asset_form.show()

    def create_asset(self):
        """ создание структуры каталога для ассета в БД ничего не заводится """
        asset_creator = AssetCreator()
        asset_type = config_frosher.ASSET_TYPES.get(self.asset_form.asset_type_cb.currentText())
        name = self.asset_form.asset_name_in.text()
        asset_creator.create_asset(config_frosher.ASSETS_ROOT, config_frosher.ASSET_STRUCTURE, asset_type, name)
        self.asset_form.asset_name_in.setText('')
        self.asset_form.hide()

    def bookmark_select(self):
        ind = self.ui.bookmarks.currentIndex()
        out = config_frosher.BOOKMARKS_DEFAULT.get(self.bookmarks.data(ind))
        out = out.replace('\\', '/')
        self.ui.project_tree.setCurrentIndex(self.directory.index(out))
        self.ui.project_tree.setExpanded(self.directory.index(out), True)
        if isinstance(out, str):
            self.update_table_model(self.current_sender)

    def set_main_style(self):
        file_of_the_style = normpath(join(self.__initial_folder, 'UI', 'style.qss'))
        with open(file_of_the_style, 'r') as f:
            style = f.read()
        self.setStyleSheet(style)
        self.setWindowTitle("eL` Frosher")
        self.setGeometry(QtCore.QRect(420, 55, 1200, 520))


class SubmitDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(SubmitDialog, self).__init__(parent)
        self.dialog = submit_dialog()
        self.dialog.setupUi(self)


class CreateAssetDialog(QtWidgets.QWidget):
    def __init__(self, parent):
        super(CreateAssetDialog, self).__init__(parent)
        self.dialog = create_asset_dialog()
        self.dialog.setupUi(self)


class LoginDialog(QtWidgets.QDialog):
    def __init__(self, *args):
        super(LoginDialog, self).__init__(*args)
        self.dialog = login_dialog()
        self.dialog.setupUi(self)
        self.ui = self.dialog
        self.setWindowTitle('Login')
        self.ui.srv_connect.setText('connect')
        self.ui.accept.setText('GO')
        self.ui.accept.clicked.connect(self.create_xui)
        self.ui.srv_connect.clicked.connect(self.connect_to_server)
        self.ticket = normpath(join(os.getenv('userprofile'), 'Documents', 'maya', 'el_frosher.json'))
        self.users = []
        _srv = os.getenv('FROSH_SERVER')
        if _srv:
            self.ui.server.setText(_srv)
        else:
            os.environ['FROSH_SERVER'] = r'o:\frosh\frosh_depot\project_files'
            _srv = os.getenv('FROSH_SERVER')
            self.ui.server.setText(_srv)
            log.debug('env FROSH_SERVER not exists, create it - {}'.format(_srv))

        try:
            self.model = QtCore.QStringListModel()
        except AttributeError:
            self.model = QtGui.QStringListModel()

        self.ui.user.setModel(self.model)

    def connect_to_server(self):
        xx = self.ui.server.text().lower()
        os.environ['FROSH_SERVER'] = xx
        _srv = os.getenv('FROSH_SERVER')
        log.info('srv - {} :: _srv - {}'.format(xx, _srv))
        db = DatabaseWorker()
        db.set_data_base(join(split(_srv)[0], 'db', 'el_frosher.db'))
        self.set_users(db.get_users())

    def set_users(self, users):
        x = [x[0] for x in users]
        # кидаем в переменную всех юзеров
        self.users = x
        # закидываем список в стринг модель
        self.model.setStringList(self.users)
        self.ui.user.setCurrentIndex(0)
        log.info(x)

    def create_xui(self):
        log.info('creating ticket...')
        fuck = {'user_name': self.ui.user.currentText(),
                'password': self.ui.password.text(),
                'workspace': self.ui.workspace.text(),
                'server': self.ui.server.text()}

        with open(self.ticket, 'w') as f:
            json.dump(fuck, f, sort_keys=True, indent=4, ensure_ascii=False)
        log.info('shit shit: {}'.format(self.ticket))
        self.accept()


class MyProgressBar(QtWidgets.QWidget):
    def __init__(self, parent):
        super(MyProgressBar, self).__init__(parent)
        self.my_pb = QtWidgets.QProgressBar()
        self.my_pb.setMinimum(0)
        self.my_pb.setMaximum(100)
        self.my_pb.setValue(0)
        self.my_pb.setParent(self)
        self.my_pb.setObjectName('progress_bar')
        self.my_pb.setTextVisible(False)

    def progress(self, file_source, file_destination):
        size_src = float(getsize(file_source))
        size_dst = float(getsize(file_destination))
        percentage = int(size_dst / size_src * 100)
        try:
            self.my_pb.setValue(percentage)
        except:
            pass

        app.processEvents()

    def copydone(self, file_source, file_destination, copied):
        self.my_pb.setValue(100)

    def copyfileobj(self, file_source, file_destination, callback_progress, callback_copydone, length=16 * 1024):

        while True:
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = FrosherFileManager()
    win.show()
    sys.exit(app.exec_())
