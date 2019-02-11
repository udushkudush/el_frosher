# -*- coding: utf-8 -*-
import sqlite3
import logging
log = logging.getLogger('elFrosher')


class DatabaseWorker:
    def __init__(self):
        self.db_file = None
        self.synchro = None
        self.project_root = None
        log.info('Primary DatabaseWorker init... {}'.format(self.db_file))

    def set_data_base(self, db_file):
        self.db_file = db_file
        # import synchronizer
        self.set_synchronizer()

    def set_synchronizer(self):
        from elFrosher.my_modules.synchro import Synchronizer
        self.synchro = Synchronizer()

    def get_users(self):
        text = "SELECT login FROM users"
        return self.read_data(text, single=False)

    def write_data(self, data):
        with sqlite3.connect(self.db_file) as db:
            cursor = db.cursor()
            cursor.execute(data)
            log.debug(u'\tначало записи\n\r')
            log.debug('record to db: {}\n\r'.format(data))
            log.debug(u'\tконец записи\n\r')
            db.commit()
            cursor.close()

    def read_data(self, request_data, single=True):
        with sqlite3.connect(self.db_file) as db:
            cursor = db.cursor()
        cursor.execute(request_data)
        if single:
            output = cursor.fetchone()
        else:
            output = cursor.fetchall()
        return output

    def path_corrector(self, path):
        # корректируем путь на проектный
        path = path.split(self.project_root)
        path = '${}/assets{}'.format('{FROSH}', path.split('assets')[-1])

        name = path.rsplit('/', 1)[-1]
        return path, name

    def get_status(self, author, filepath):
        text = """SELECT id, file, version,
(SELECT version FROM local_version
WHERE user_id=(select id from users where login='{0}') AND asset_id = assets.id) as local_ver,
(SELECT status_id FROM checkout WHERE checkout.asset_id = assets.id) as checkout,
(select users.login from users where users.id = (SELECT user_id
FROM checkout WHERE checkout.asset_id = assets.id)) as editor
FROM assets WHERE file = '{1}'""".format(author, filepath)
        result = self.read_data(text)
        return result

    def get_row_keys(self, table_name):
        data = "SELECT * FROM '{}'".format(table_name)
        with sqlite3.connect(self.db_file) as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
        cursor.execute(data)
        xx = cursor.fetchone()
        # print(xx.keys())
        # output = [x[1] in x for x in xx]
        try:
            header = xx.keys()
        except AttributeError:
            header = ['nooooope', 'nooooope', 'nooooope']
        return header

    def get_dict(self, author, *args):
        # получаем словарь из списка всех ассетов в базе данных, на выходе имеем формат:
        # dict(absoluteLocalFilePath: [version, local_version, checkout, editor, asset.id])

        sub1 = "SELECT id FROM users where login='{}'".format(author)
        sub2 = "SELECT user_id FROM checkout WHERE checkout.asset_id = assets.id"
        request = """
SELECT id, file, version, 
(SELECT version FROM local_version where user_id = ({sub_request_1}) AND asset_id = assets.id) AS local_ver,
(SELECT status_id FROM checkout WHERE checkout.asset_id = assets.id) as checkout,
(SELECT users.login FROM users WHERE users.id = ({sub_request_2})) as editor
FROM assets""".format(sub_request_1=sub1, sub_request_2=sub2)

        x = self.read_data(request, single=False)

        data = {}
        # local = project.replace('\\', '/')
        for a in x:
            # print('dicty iter ', a[1].replace('${FROSH}', ''))
            # отсекаем переменную, корень пути будем прибавлять там где потребуется этот словарь
            data[a[1].replace('${FROSH}', '')] = [a[2], a[3], a[4], a[5], a[0]]
        return data

    def get_simple_dict(self):
        # получаем словарь из списка всех ассетов в базе данных, на выходе имеем формат:
        request = """SELECT file FROM assets"""
        # print('project root: ', self.project_root, '\ndb file: ', self.db_file)

        x = self.read_data(request, single=False)

        local = self.project_root.replace('\\', '/')
        data = [a[0].replace('${FROSH}', local) for a in x]

        return data

    def change_status(self, filelist, user):
        # функция смены статуса файла, типа взять в работу и все такое
        # работает со списком файлов
        checkout = True
        skippedfiles = []
        for f in filelist:
            # корректируем путь
            __, __, file = self.synchro.splitter(f)
            file = file.replace('\\', '/')
            res = self.get_status(user, file)
            # id, filePath, version, localVersion, isChekout, editor
            # print(res)
            # сначала удостоверимся что у юзера финальная версия файла
            if res:
                asset_id, file_path, version, local_version, is_checkout, editor = res
                log.debug('is checkout: {}\t editor: {}\t user: {}'.format(is_checkout, editor, user))
                # print('\n\r', is_checkout, '\t', editor, '\t', user)
                if is_checkout:
                    if editor != user:
                        # print(u'файл в работе у ', editor)
                        skippedfiles.append('файл в работе у {}'.format(f))
                        continue
                    elif editor == user:
                        text = """DELETE FROM checkout WHERE asset_id = '{}' AND user_id = (
                        SELECT users.id FROM users WHERE login = '{}')""".format(asset_id, user)
                        # print(u'хм.. зассал значит редактировать...')
                        self.write_data(text)

                elif int(version) > int(local_version):
                    skippedfiles.append('локальная версия устарела {}'.format(f))
                    # print(u'обнови до свежей версии прежде чем брать в работу')
                    continue
                elif not local_version:
                    skippedfiles.append('файл не синхронизирован {}'.format(f))
                    # print(u'сначала файл надо себе скопировать')
                    continue
                else:
                    # print('checkout ', checkout)
                    log.info('checkout {}\n\r'.format(checkout))
                    # вношу в таблицу checkout автора и ИД ассета
                    # статус ИД для чекаута - 4
                    text = """insert into checkout (asset_id, status_id, user_id)
values ((select id from assets where file = '{file}'), 4,
(select id from users where login='{editor}'))""".format(file=file, editor=user)
                    # print('\n', text, '\n\r', editor, '\t', user)
                    self.write_data(text)

                    # res = self.get_status(user, file)
                    # print('берем в работу или снимаем статус чекаут.\n\r\rпроверка из базы ', res)
            else:
                skippedfiles.append('файла нет на сервере {}'.format(f))
                # print(u"на сервере нет такого файла")
                # print('запиь в базе ', res)

    def get_version(self, filename, author, version):
        # функция копировани файла на локал, копируем и записываем в таблице local_version
        # todo приделать триггер на проверку составного ключа и либо обновить либо добавить запись

        # запускаем копирование файла
        # print('\nget_version: ', filename)
        self.synchro.sync_file(filename, version)

        log.debug('db: copy this file: {}'.format(filename))
        # сначала делаем апдейт в таблице local_version, если записи нет запрос проигнорируется
        text = """UPDATE local_version SET version='{0}'
WHERE user_id=(select id from users where login='{1}')
AND asset_id=(SELECT assets.id FROM assets WHERE file = '{2}')""".format(version, author, filename)
        self.write_data(text)

        # теперь вставляем запись local_version, если запись уже есть, то запрос проигнорируется
        text = """INSERT OR IGNORE INTO local_version (user_id, asset_id, version)
VALUES ((select id from users where login='{}'), (SELECT assets.id FROM assets WHERE file = '{}'),
'{}')""".format(author, filename, version)
        self.write_data(text)
        log.info('UPDATE LOCAL VERSION')

    def multiple_assets_records(self, assetlist, author, status=1, comment=None):
            """ создаем общий пендинл лист для выбранных ассетов """
            # author = self.get_author(author)

            " завернуть номер пендинг листа в запрос "
            pending = "SELECT MAX(pending.id) FROM pending"
            pending_list = self.read_data(pending)[0] or None
            if not pending_list:
                pending_list = 1
            else:
                pending_list += 1

            if not comment:
                comment = 'no comment'
            else:
                # comment = comment.decode('utf-8')
                print('comment nodecode: {}'.format(comment))
                # print('comment decode: {}'.format(comment.encode('cp1251')))

            ''' теперь надо обработать список выделеных файлов '''
            'сначала добавляем список файлов по таблицам asset и pending'
            skipped_files = []
            for file in assetlist:
                asset_id, srv_path, version, local_version, checkout, editor = '', '', '', '', '', ''

                # проверка есть ли запись об ассете в базе, если есть то обновляется версия,
                # если записи нет,  тогда добавляем ее
                __, name, filepath = self.synchro.splitter(file)

                # конвертация в виндовых слешей, пусть в базе хранятся с обратными слешами
                filepath = filepath.replace('\\', '/')

                # формируем запрос для проверки
                text = """SELECT id, file, version,
(SELECT version FROM local_version
WHERE user_id=(select id from users where login='{user}')
AND asset_id = assets.id) as local_ver,
(SELECT status_id FROM checkout WHERE checkout.asset_id = assets.id) as checkout,
(select users.login from users where users.id = (
SELECT user_id FROM checkout WHERE checkout.asset_id = assets.id)) as editor
FROM assets WHERE file = '{file}'""".format(user=author, file=filepath)
                result = self.read_data(text)

                # распаковываем результат по переменным, result вернет None если в БД нет записи об ассете
                if result:
                    asset_id, srv_path, version, local_version, checkout, editor = result
                # print('id: {}\tfile: {}\tver: {} local: {}\t\tcheckout: {} editor:{} receiver: {}'.format(
                #     asset_id, srv_path, version, local_version, checkout, editor, author))

                # если есть ID, значит файл уже проведен в базе
                if asset_id:
                    # тогда сверяем версии, и далее проверяем не висит ли на нем статус в работе'
                    if local_version != version:
                        # если версии не совпадают файл пропускаем
                        skipped_files.append('skipped>> local_version != version: {}'.format(filepath))
                        # log.info('skipped>> local_version != version: {}'.format(filepath))
                        # print(u'пропуск: >> \t', filepath)
                        continue
                    elif checkout and editor != author:
                        # если висит статус чекаут, сверяемся совпадают ли автор запроса и редактор, при несовпадении
                        # - пропускаем файл и меняем статус с 1 на None
                        # print('file: {} checkout: {}\teditor: {}\tauthor: {}'.format(srv_path, checkout, editor, author))
                        # status = None
                        skipped_files.append('skipped>> checkout and editor != author: {}'.format(filepath))
                        # log.info('skipped>> checkout and editor != author: {}'.format(filepath))
                        continue
                    elif checkout and editor == author:
                        # редактор и автор запроса совпадают, при сабмите снимаем статус checkout
                        status = 1
                        log.info('checkout detect, editor : {} | author : {}, switch status on : {}'.format(
                            editor, author, status))
                        # print(u'checkout детектед, редактор : {}, автор : {}, ставим статус на {}'.format(editor, author, status))

                    # файл прошел все проверки и уже есть запись в базе, добавляем 1 к номеру версии
                    version = int(version) + 1
                    text = """UPDATE assets SET version='{}' WHERE assets.id = '{}'""".format(version, asset_id)
                    self.write_data(text)

                    # заливаем файло на сервак, вписываем итерируемый объект, с локальным путем, так как
                    # synchro определяет направление копирования исходя из поданого пути
                    log.info(u'заливаем файло на сервак:\n\rfile: {}\tversion: {}'.format(file, version))
                    # print(u'заливаем файло на сервак:\n\rfile: {}\tversion: {}'.format(file, version))
                    self.synchro.sync_file(file, version)
                    # print(text)

                    # и сразу заносим в пендинг лист
                    text = """INSERT INTO pending (id, asset_id, version)
                    VALUES ('{}','{}','{}')""".format(pending_list, asset_id, version)
                    self.write_data(text)
                    # print(text)

                    # заводим статус в чекаут
                    if status == 4:
                        text = "INSERT INTO checkout (asset_id, status_id, user_id ) VALUES ('{}','{}','{}')".format(
                            asset_id, status, author['id'])
                        self.write_data(text)
                        # print(text)
                    elif status == 1:
                        text = """DELETE FROM checkout WHERE asset_id = '{}' AND user_id = (SELECT users.id FROM users
                        WHERE login = '{}')""".format(asset_id, author)
                        self.write_data(text)

                    # прописываем в журнал номер локальной версии
                    text = """INSERT OR REPLACE INTO local_version (user_id, asset_id, version)
                        VALUES ((SELECT user_id FROM local_version WHERE user_id = (
                        SELECT id FROM users WHERE users.login = '{}')),
                        (SELECT asset_id FROM local_version WHERE asset_id = '{}'), '{}')""".format(
                            author, asset_id, version)
                    # print(text, '\n\n')
                    self.write_data(text)

                else:
                    # asset_id = None, значит записи в БД нет, добавляем запись в таблицу ассетов, версия - 1
                    print(u'\rновая запись\n\n\r')
                    version = 1
                    text = """INSERT INTO assets (file, name, version) VALUES ('{}', '{}', '{}')""".format(
                        filepath, name, version)
                    # print(text)
                    self.write_data(text)

                    # todo надо объединить запись нового ассета в один запрос
                    # теперь забираем его айдишник
                    text = "SELECT assets.id FROM assets WHERE file = '{}'".format(filepath)
                    asset_id = self.read_data(text)[0]
                    'добавляем этот файл в тот же пендинг лист'
                    text = "INSERT INTO pending (id, asset_id, version) VALUES ('{}','{}','{}')".format(
                        pending_list, asset_id, version)
                    # print(text)
                    self.write_data(text)

                    # заливаем файло на сервак
                    log.info('copy to server: {}\t- version: {}'.format(file, version))
                    # print(u'заливаем файло на сервак:\n\rfile: {}\tversion: {}'.format(file, version))
                    self.synchro.sync_file(file, version)

                    # заводим статус в чекаут
                    if status == 4:
                        text = """INSERT INTO checkout (asset_id, status_id, user_id )
                        VALUES ('{}','{}','{}')""".format(asset_id, status, author)
                        self.write_data(text)
                        # print(text)
                    # делаем запись в таблице учета локальных версий
                    text = """INSERT INTO local_version (user_id, asset_id, version)
                    VALUES ((SELECT id FROM users WHERE login= '{}'), '{}', '{}')""".format(
                        author, asset_id, version)
                    self.write_data(text)
                    # print(text, '\n\n')
            # теперь добавляем запись в таблицу info
            # todo если файл в списке один и он пропущен то пендинг создается, надо разрулить этот момент
            if skipped_files:
                if len(assetlist) == len(skipped_files):
                    log.info('нет добавляемых файлов')
                    # print(u'нет добавляемых файлов')
            else:
                text = """INSERT INTO info (pending_id, author_id, comment, date)
VALUES ('{}', (SELECT id FROM users WHERE login= '{}'), '{}', datetime("now", "localtime"))""".format(
                    pending_list, author, comment)
                log.info(text)
                self.write_data(text)

            # выводим список пропущенных файлов
            if skipped_files:
                log.info('пропущенные файлы:\n\n\n')
                # print(u'\n\n\nпропущенные файлы: ')
                for s in skipped_files:
                    log.info(s)
                    # print('skip: > {}'.format(s))

    def create_tables(self):
        # функция быстро создает все нужные таблицы со связями
        tables = {
            'table_asset': """assets (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
stage_id INTEGER,
file TEXT NOT NULL UNIQUE,
file_pm TEXT,
version INTEGER NOT NULL,
inputs_id INTEGER,
FOREIGN KEY (stage_id) references stage(id)
FOREIGN KEY (inputs_id) references inputs(id)
)""",
            'table_info': '''info (
id INTEGER PRIMARY KEY AUTOINCREMENT,
pending_id INTEGER,
author_id INTEGER,
comment TEXT,
date TEXT,
preview_id INTEGER,
FOREIGN KEY (author_id) REFERENCES users(id),
FOREIGN KEY (preview_id) REFERENCES preview(id)
)''',
            'table_pending': '''pending (
id INTEGER,
asset_id INTEGER,
version INTEGER,
FOREIGN KEY (id) REFERENCES info(pending_id)
)''',
            'table_local_version': '''local_version(
user_id INTEGER NOT NULL,
asset_id INTEGER NOT NULL,
version INTEGER NOT NULL,
FOREIGN KEY (user_id) REFERENCES users(id),
FOREIGN KEY (asset_id) REFERENCES assets(id),
PRIMARY KEY (user_id, asset_id)
)''',
            'table_users': '''users (
login TEXT NOT NULL UNIQUE,
id INTEGER PRIMARY KEY AUTOINCREMENT,
email TEXT,
group_id INTEGER,
FOREIGN KEY (group_id) REFERENCES groups(id)
)''',
            'table_inputs': '''inputs (
list_id INTEGER,
scene_id INTEGER,
path TEXT,
FOREIGN KEY (scene_id) REFERENCES assets(id),
FOREIGN KEY (path) REFERENCES assets(path)
)''',
            'table_status': '''status (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL UNIQUE)''',
            'table_previews': '''preview (
id INTEGER PRIMARY KEY AUTOINCREMENT,
picture BLOB
)''',
            'table_groups': '''groups (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL UNIQUE
)''',
            'table_stage': '''stage (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL UNIQUE
)''',
            'table_tempRecord': '''temp_record(
pending_id INTEGER NOT NULL,
asset_id INTEGER NOT NULL,
file TEXT NOT NULL,
name TEXT NOT NULL,
author_id INTEGER NOT NULL,
status_id INTEGER NOT NULL,
comment TEXT NOT NULL,
version INTEGER NOT NULL,
date_modify TEXT NOT NULL
) ''',
            'table_checkout': '''checkout(
asset_id INTEGER NOT NULL UNIQUE,
status_id INTEGER NOT NULL,
user_id INTEGER NOT NULL,
FOREIGN KEY (asset_id) REFERENCES assets(id),
FOREIGN KEY (status_id) references status(id),
FOREIGN KEY (user_id) REFERENCES users(id),
PRIMARY KEY (asset_id, user_id)
)'''}
        with sqlite3.connect(self.db_file) as db:
            cursor = db.cursor()
            for t in tables:
                xx = 'CREATE TABLE IF NOT EXISTS {}'.format(tables.get(t).replace('\n', ' '))
                # print(xx)
                cursor.execute(xx)
                db.commit()
            cursor.close()
