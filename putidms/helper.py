# -*- coding:utf-8 -*-

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    r = enums
    enums['to_dict'] = dict((key, value) for key, value in enums.iteritems())
    enums['r'] = r
    return type('Enum', (), enums)
