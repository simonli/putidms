# -*- coding:utf-8 -*-


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    enums['to_dict'] = dict((key, value) for key, value in enums.iteritems())
    return type('Enum', (), enums)
