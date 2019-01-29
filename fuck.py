# -*- coding: utf-8 -*-
from PySide2 import QtCore, QtWidgets, QtGui
from elFrosher.my_modules.asset_creator import AssetCreator
from elFrosher.my_modules.DataBaseWorker import DatabaseWorker
from elFrosher.my_modules.synchro import Synchronizer
from elFrosher.models.models import DataBaseViewer, ServerTreeModel, TableDetailsViewer

from elFrosher.my_modules import config
from elFrosher.UI.main_window import Ui_MainWindow as myFuckingWindow
from elFrosher.UI.submit_form import Ui_submit_dialog as submit_dialog
from elFrosher.UI.create_asset_form import Ui_Form as create_asset_dialog
from os.path import dirname, join, normpath
import sys


class SomeFuckingShit(QtWidgets.QMainWindow):
    __initial_folder = dirname(__file__)
    __DATABASE = normpath(join(__initial_folder, 'db', 'tmp_work.db'))
    asset_form, submit_form = '', ''
    directory, server = '', ''

    project_root = normpath(config.PROJECT)
    server_root = normpath(config.SERVER)
    versions = normpath(config.VERSIONS)

    def __init__(self, *args):
        super(SomeFuckingShit, self).__init__(*args)
        self.synchro = Synchronizer()
        self.db = DatabaseWorker(self.__DATABASE)
        self.db.project_root = config.PROJECT
        self.fileslist = []
        self.current_sender = None
        self.ui = myFuckingWindow()
        self.ui.setupUi(self)

        self.ico_download = QtGui.QPixmap(normpath(join(self.__initial_folder, 'icons', 'arrow_down.png')))
        self.ico_check = QtGui.QPixmap(normpath(join(self.__initial_folder, 'icons', 'check.png')))
        self.ico_increment = QtGui.QPixmap(normpath(join(self.__initial_folder, 'icons', 'incremental.png')))
        self.ico_submit = QtGui.QPixmap(normpath(join(self.__initial_folder, 'icons', 'arrow-up.png')))
        self.ico_folder = QtGui.QPixmap(normpath(join(self.__initial_folder, 'icons', 'folder.png')))

        self.buttons()
        self.setup_all_ui()
        self.set_main_style()
        self.setup_signals()

        # ---- bookmarks defaults ---- #
        try:
            self.bookmarks = QtCore.QStringListModel()
        except AttributeError:
            self.bookmarks = QtGui.QStringListModel()

        bookmarks = []
        for i in config.BOOKMARKS_DEFAULT:
            bookmarks.append(i)
        self.bookmarks.setStringList(bookmarks)
        self.ui.bookmarks.setModel(self.bookmarks)
        # переменныю для таблиц
        self.table_model = ''
        self.table_details_model = ''
        self.init_table()

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
        self.ui.user_name.setText(config.user)

    def setup_all_ui(self):
        # ---- DIALOGS ----- #
        self.submit_form = SubmitDialog()
        self.asset_form = CreateAssetDialog()

        # ---- splitters ---- #
        self.ui.horizontal_left_splitter.setSizes([150, 350])
        self.ui.vertical_splitter.setSizes([250, 300])

        # ---- TREE VIEW ----- #
        self.directory = ServerTreeModel()
        self.server = ServerTreeModel()

        # dicty = self.db.get_dict(self.project_root, config.user)
        # self.directory.update(dicty, self.project_root)
        self.updater_tree_model(self.directory, self.project_root)
        self.directory.setpath(self.project_root)
        # ----- set project dir in tree view ----- #
        main_tree = self.ui.project_tree
        main_tree.setModel(self.directory)
        main_tree.setRootIndex(self.directory.index(self.project_root))
        # main_tree.expanded.connect(self.expander)
        main_tree.setColumnHidden(1, True)
        main_tree.setColumnHidden(2, True)
        main_tree.setColumnHidden(3, True)
        main_tree.setColumnWidth(0, 210)
        main_tree.setHeaderHidden(True)
        main_tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        main_tree.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # main_tree.clicked.connect(lambda zz: s'lol'))
        main_tree.customContextMenuRequested.connect(self.context_project_tree)

        server_tree = self.ui.server_tree
        # self.server.update(dicty, self.server_root)
        self.updater_tree_model(self.server, self.server_root)
        self.server.setpath(self.server_root)
        server_tree.setModel(self.server)
        server_tree.setRootIndex(self.server.index(self.server_root))
        server_tree.setColumnHidden(1, True)
        server_tree.setColumnHidden(2, True)
        server_tree.setColumnHidden(3, True)
        server_tree.setHeaderHidden(True)
        server_tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        server_tree.customContextMenuRequested.connect(self.context_server_tree)

    def setup_signals(self):
        # сигналы для деревьев
        self.ui.project_tree.selectionModel().selectionChanged.connect(self.click_project_tree)
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

    def updater_tree_model(self, model, model_root):
        dicty = self.db.get_dict(config.user)
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
            # print('search input: ', search)
            # select pending, name, file from main_info where file like '%/assets/chars%'
            data = """SELECT pending, comment, author, submit_date
                FROM '{}' WHERE file LIKE '%{}%'""".format(table, search)
        else:
            data = "SELECT pending, comment, author, submit_date FROM '{}'".format(table)
        data = self.db.read_data(data, single=False)
        # очищаем список от дублирующих записей и сортируем по номеру пенд листа
        data = sorted(list(set(data)), key=lambda k: k[0])
        header = ['list', 'comment', 'author', 'data']
        return data, header

    def init_table(self):

        data, header = self.table_prepare_data()
        details = self.ui.details_table
        pending = self.ui.pending_table
        if not data:
            data = [('записей', 'не', 'найдено'), ('прям', 'ваще нахуй', 'пусто')]
            # print('init table...')
        data2 = [('', 'выбери ', '', 'что-нибудь в верхнейтаблице')]
        header2 = ['(.)(.)', '(.)', '(.)(.)', '(.)']
        self.table_model = DataBaseViewer(data, header)
        self.table_details_model = DataBaseViewer(data2, header2)

        pending.setModel(self.table_model)
        details.setModel(self.table_details_model)

        pending.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        pending.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        pending.verticalHeader().hide()
        pending.setColumnWidth(0, 48)
        pending.setColumnWidth(1, 450)
        pending.setColumnWidth(2, 150)
        pending.setColumnWidth(3, 85)

        details.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        details.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        details.verticalHeader().hide()
        details.setColumnWidth(0, 48)
        details.setColumnWidth(1, 210)
        details.setColumnWidth(2, 48)
        details.setColumnWidth(3, 420)
        # pending.customContextMenuRequested.connect(self.context_table)
        # self.ui.details_table.verticalHeader().setSectionSize(15)

    def update_table_model(self, sender=None):
        if sender == 'server':
            self.current_sender = self.ui.server_tree
        else:
            self.current_sender = self.ui.project_tree
        # забираем текущий индекс из дерева
        info = self.current_sender.model().filePath(self.current_sender.currentIndex())

        # удаляем префикс из пути файла
        search = normpath(info).split(self.project_root)[-1].split(self.server_root)[-1]
        search = search.replace('\\', '/')

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
            # print('this_file', this_file, ' and rev number is: ', version)
            self.get_version(this_file, version)
            self.update_table_model(this_file)

    def click_project_tree(self):
        self.ui.submit.setEnabled(True)
        # устанавливаем в переменную сендера, так как он может быть использован в других коммандах
        self.current_sender = self.sender()

        # а пока обновляем данные из БД
        _inf = self.current_sender.model().fileInfo(self.current_sender.currentIndex())
        if not _inf.isDir():
            self.fileslist = self.file_collector()
            p = normpath(self.fileslist[-1]).replace(self.project_root, '${FROSH}').replace('\\', '/')
            text = "SELECT asset_id, name, history, file FROM main_info WHERE file = '{}'".format(p)
            data = self.db.read_data(text, single=False)
            header = ['id', 'file name', 'version', 'path']
            self.table_updater(self.table_details_model, data, header)
            self.update_table_model()

    def click_server_tree(self):
        self.ui.submit.setEnabled(False)
        self.update_table_model('server')

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
        self.fileslist = self.file_collector()

        if action == get_latest:
            self.get_version()
        elif action == checkout:
            self.checkout()
        elif action == submit:
            # x = self.sender()
            # print(x)
            # self.current_sender = x
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
        view = self.ui.project_tree
        if sender:
            view = sender
        model = view.model()
        _ind = view.selectionModel().selectedIndexes()
        indexes = [x for x in _ind if x.column() == 0]
        fileslist = [normpath(model.filePath(x)) for x in indexes if not model.fileInfo(x).isDir()]

        return fileslist

    def submit_clicked(self):
        self.current_sender = self.ui.project_tree
        self.fileslist = self.file_collector()
        self.submit_form.show()

    def get_version_clicked(self):
        self.fileslist = self.file_collector()
        self.get_version()

    def submit_func(self):
        """сабмит ебана"""
        # сабмитить можно только с локального дерева, значит выставляем его в качестве текущего сендера
        self.current_sender = self.ui.project_tree
        comment = self.submit_form.dialog.comment.toPlainText()
        if comment:
            comment = comment.encode('utf-8')
        author = config.user
        # собираем список файлов чтобы оформить пакет для отправки в БД
        # 'проверка на валидность что-ли'
        if len(self.fileslist) > 0:
            # print(self.fileslist, author, comment, '\n________')
            ' отправляем сразу весь список файлов в БД '
            self.db.multiple_assets_records(self.fileslist, author, comment=comment)
            ' обновляем таблицу представления из БД '
            self.update_table_model()
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
        author = config.user

        """если не указан файл значит юзер сделал запрос из дерева, тогда просто вызываем файлколлектор
            и обновляем список выбранных ассетов до последних версий"""
        if not filename:
            for f in self.fileslist:
                # забираем из БД самую последнюю версию файла
                if not ver:
                    __, __, f = self.synchro.splitter(f)

                    f = f.replace('\\', '/')
                    request_data = "SELECT version FROM assets WHERE assets.file='{}'".format(f)
                    ver = self.db.read_data(request_data)[0]

                self.db.get_version(f, author, ver)
            # обнуляем список выбранных файлов
            self.fileslist = []
        else:
            # из таблицы можно выбрать только одну версию
            self.db.get_version(filename, author, ver)

        # обновляем деревья
        self.update_tree_views(self.ui.project_tree, self.directory, self.project_root)
        self.update_tree_views(self.ui.server_tree, self.server, self.server_root)

    def checkout(self):
        # " функция почемает файл в работу "
        # и отправляем в датабэйзера список файлов и сразу обнуляем его
        self.db.change_status(self.fileslist, config.user)
        self.fileslist = []
        self.update_tree_views(self.ui.project_tree, self.directory, self.project_root)
        self.update_tree_views(self.ui.server_tree, self.server, self.server_root)

    def show_asset_create(self):
        self.asset_form.asset_type_cb.clear()
        for i in config.ASSET_TYPES:
            self.asset_form.asset_type_cb.addItem(i)
        self.asset_form.show()

    def create_asset(self):
        """ создание структуры каталога для ассета в БД ничего не заводится """
        asset_creator = AssetCreator()
        asset_type = config.ASSET_TYPES.get(self.asset_form.asset_type_cb.currentText())
        name = self.asset_form.asset_name_in.text()
        asset_creator.create_asset(config.ASSETS_ROOT, config.ASSET_STRUCTURE, asset_type, name)
        self.asset_form.asset_name_in.setText('')
        self.asset_form.hide()

    def bookmark_select(self):
        ind = self.ui.bookmarks.currentIndex()
        out = config.BOOKMARKS_DEFAULT.get(self.bookmarks.data(ind))
        out = out.replace('\\', '/')
        self.ui.project_tree.setCurrentIndex(self.directory.index(out))
        self.ui.project_tree.setExpanded(self.directory.index(out), True)
        if isinstance(out, str):
            self.update_table_model(out)

    def set_main_style(self):
        file_of_the_style = normpath(join(self.__initial_folder, 'UI', 'style.qss'))
        with open(file_of_the_style, 'r') as f:
            style = f.read()
        self.setStyleSheet(style)
        self.setWindowTitle("eL` Frosher")
        self.setGeometry(QtCore.QRect(420, 55, 850, 520))


class SubmitDialog(QtWidgets.QDialog):
    def __init__(self):
        super(SubmitDialog, self).__init__()
        self.dialog = submit_dialog()
        self.dialog.setupUi(self)


class CreateAssetDialog(QtWidgets.QWidget):
    def __init__(self):
        super(CreateAssetDialog, self).__init__()
        self.dialog = create_asset_dialog()
        self.dialog.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = SomeFuckingShit()
    win.show()
    sys.exit(app.exec_())
