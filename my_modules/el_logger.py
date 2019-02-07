import logging


class ElLogger(object):
    def __init__(self, name, file):
        super(ElLogger, self).__init__()
        self.name = None
        self.file = file
        self.log = logging.getLogger(name)
        self.log.setLevel(logging.DEBUG)

        fh = logging.FileHandler(file, mode='w', encoding='utf-8')
        formatter = logging.Formatter(u'%(levelname)-8s | %(lineno)-3d | %(module)-18s | [%(asctime)s] | %(message)s')
        fh.setFormatter(formatter)
        self.log.addHandler(fh)

