import logging
from os.path import exists, normpath, join, split
from os import getenv


class ElLogger(object):
    def __init__(self):
        super(ElLogger, self).__init__()
        self.name = None
        self.file = None
        self.log = None

    def set_name(self, name):
        self.name = name
        self.log = logging.getLogger(name)
        self.log.setLevel(logging.DEBUG)

    def set_log_file(self, file):
        if exists(file):
            self.file = file
        else:
            _pth, name = split(getenv('userprofile'))
            self.file = normpath(join(_pth, name, 'Documents', 'maya', 'log_{}.txt'.format(name)))
        fh = logging.FileHandler(self.file, mode='w', encoding='utf-8')
        x = u'%(levelname)-8s | %(lineno)-3d | %(module)-18s | %(funcName)s | [%(asctime)s] | %(message)s'
        formatter = logging.Formatter(x)
        fh.setFormatter(formatter)
        self.log.addHandler(fh)

    # def set_file_handler(self):
    #     fh = logging.FileHandler(self.file, mode='w', encoding='utf-8')
    #     x = u'%(levelname)-8s | %(lineno)-3d | %(module)-18s | %(funcName)s | [%(asctime)s]\n\t\t\t %(message)s'
    #     formatter = logging.Formatter(x)
    #     fh.setFormatter(formatter)
    #     self.log.addHandler(fh)
