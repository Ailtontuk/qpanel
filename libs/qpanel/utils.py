# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

import ConfigParser
from datetime import timedelta
import time
from config import QPanelConfig


def unified_configs(file_config, file_template, sections=[]):

    config = QPanelConfig(file_config).config
    template = QPanelConfig(file_template).config

    # create new file based in template
    for s in sections:
        items = dict(template.items(s))
        for i in items:
            try:
                template.set(s, i,  config.get(s, i))
            except:
                pass

    # set old configs
    for s in config.sections():
        items = dict(config.items(s))
        for i in items:
            try:
                template.set(s, i,  config.get(s, i))
            except ConfigParser.NoSectionError:
                template.add_section(s)
                template.set(s, i,  config.get(s, i))

    file = open(file_config, 'wr')
    template.write(file)
    file.close()


# http://stackoverflow.com/a/6425628
def underscore_to_camelcase(word):
    """
        Convert word to camelcase format
    """
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def clean_str_to_div_id(value):
    """ Clean String for a div name.
        Convert character like @ / and . for more easy use in JQuery
        Parameter: value = string
    """
    v = value.replace('/', '-')
    v = v.replace('.', '_')
    return v.replace('@', '_')


def timedelta_from_field_dict(field, dic, current_timestamp=None,
                              is_seconds_ago=False):
    seconds_ago = 0
    if not current_timestamp:
        current_timestamp = time.time()
    if field in dic:
        if int(dic[field]) > 0:
            if is_seconds_ago:
                seconds_ago = int(dic[field])
            else:
                seconds_ago = int(current_timestamp) - int(dic[field])

    return timedelta(seconds=seconds_ago)


def convert_time_when_param(value, splitter=','):
    var = value.split(splitter)
    hour = '00:00:00'
    if len(var) > 1:
        hour = var[1].strip()
    try:
        hour = time.strptime(hour, "%H:%M:%S")
    except:
        hour = time.strptime('00:00:00', "%H:%M:%S")
    hour = time.strftime('%M:%M:%S', hour)
    return {'when': var[0], 'hour': hour}
