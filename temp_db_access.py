# -*- coding: utf-8 -*-
from elFrosher.my_modules.DataBaseWorker import DatabaseWorker
from os.path import join, dirname, normpath, exists, split
from os import makedirs
from elFrosher.my_modules import config_frosher


# current_dir = dirname(__file__)

current_dir = split(config_frosher.SERVER)[0].replace('\\', '/')

file = normpath(join(current_dir, 'db', 'el_frosher.db'))

if not exists(normpath(split(file)[0])):
    makedirs(split(file)[0])


db = DatabaseWorker(file)
print('create or update db... ', file)


def fill_some_tables():
    # заполнение новой БД
    stage = [
        'scetch',
        'model',
        'rig',
        'texture',
        'shading',
        'fur',
        'render',
        'composing'
    ]
    status = [
        'normal',
        'add',
        'delete',
        'checkout'
    ]
    for s in stage:
        text = "INSERT OR IGNORE INTO stage (name) VALUES ('{}')".format(s)
        db.write_data(text)

    for a in status:
        text = "INSERT OR IGNORE INTO status (name) VALUES ('{}')".format(a)
        db.write_data(text)

    data = ['a.polomoshnov', 'a.ryazantsev', 'a.romashkina', 'v.verkhozin', 'v.borzenko', 't.khoroshih', 'y.sysoev']

    for d in data:
        text = "INSERT OR IGNORE INTO users (login, email) VALUES ('{}', '{}')".format(d, d + '@souzmult.ru')
        db.write_data(text)

    groups = [
        'painters',
        'animators',
        'modelers',
        'editors',
        'shading'
    ]
    for g in groups:
        text = "INSERT OR IGNORE INTO groups(name) VALUES ('{}')".format(g)
        db.write_data(text)


def add_record():
    path_to_file = "C:/DEV/local/assets/chars/zaloopa/zaloopa_konskaya.ma"
    path_to_file = "C:/DEV/local/assets/chars/frosh/rig_frosh.ma"
    files = ["C:/DEV/local/assets/chars/frosh/rig_frosh.ma"]

    author = 'a.polomoshnov'
    comment = "шейдинг в процессе"
    # author = 'a.ryazantsev'
    # comment = "уменьшил левое яйцо, добавлена асиметрия на залупу"
    db.multiple_assets_records(files, author)


def create_trigger():
    trigger01 = '''CREATE TRIGGER update_pending AFTER INSERT ON info
     BEGIN
         UPDATE pending SET local_ver = new.version
         WHERE asset_id = new.asset_id AND user_id=new.author_id;
    END;'''

    trigger02 = """CREATE TRIGGER fill_tables AFTER INSERT ON temp_record
    BEGIN
        
        INSERT INTO assets (name, file, status_id, version)
        VALUES (new.name, new.file, new.status_id, new.version);
        
        INSERT INTO info (pending_id, author_id, comment, version, date)
        VALUES (new.pending_id, new.author_id, new.comment, new.version, new.date_modify);
        
        INSERT INTO pending (id, asset_id, version)
        VALUES (new.pending_id, new.asset_id, new.version);
        
        DELETE FROM temp_record WHERE rowid=1;
    END;"""

    trigger03 = """CREATE TRIGGER tableFiller AFTER INSERT ON temp_record
    BEGIN
    CASE
    WHEN (SELECT MAX(version), assets.id FROM assets WHERE file = new.file)
    
    """
    db.write_data()


def selection_test():
    text = """
select pending.version as 'history', (select file from assets where assets.id = pending.asset_id) as 'file path',
(select comment from info where info.pending_id = pending.id) as comment,
(select users.login from users where users.id = (
select info.author_id from info where info.pending_id = pending.id)) as 'editor',
(select info.date from info where info.pending_id = pending.id) as 'date modify'
from pending order by 'file path'
            """

    x = db.read_data(text, single=False)
    for i in x:
        print(i)


def create_view():

    views = {
        'view01': """CREATE VIEW IF NOT EXISTS main_info
        AS SELECT
            info.pending_id AS pending,
            assets.name AS name,
            assets.id AS asset_id,
            (select users.login from users where users.id = info.author_id) AS author,
            info.comment AS comment,
            assets.version AS rev,
            (SELECT pending.version FROM pending WHERE pending.asset_id = assets.id AND pending.id = info.pending_id) AS history,
            info.date AS submit_date,
            assets.file AS file
        FROM info
        INNER JOIN pending ON info.pending_id = pending.id
        INNER JOIN assets ON (SELECT pending.asset_id = assets.id WHERE pending.id = info.pending_id)
        """,
        'view02': """CREATE VIEW IF NOT EXISTS pending_view
        AS SELECT
            info.pending_id AS pending,
            users.login AS author,
            info.comment AS comment,
            info.date AS submit
        FROM info
        INNER JOIN users ON info.author_id = users.id
        """,
        'view03': """create view if not exists 'CHECKOUT_TABLE'
        as select 
            checkout.asset_id as 'ID',
            assets.name as 'NAME',
            (select users.login from users where users.id = checkout.user_id) as 'EDITOR',
            assets.file as 'PATH'
        from checkout
        inner join assets on checkout.asset_id = assets.id"""}

    for a in views:
        print(views[a])
        db.write_data(views[a])


def test_dict():
    xx = db.get_dict('D:/frosh', 'v.borzenko')
    print('ключи\t\t', xx.keys(), '\n')
    info = 'assets'
    catch = [a for a in xx.keys() if info in a]
    for a in xx.keys():
        if info in a:
            break
    print(catch)


db.create_tables()
fill_some_tables()
create_view()

# test_dict()
# create_trigger()
# selection_test()
# add_record()
# db.multiple_assets_records()

