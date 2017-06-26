#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os
import glob
import datetime
import time
import redis
import logging
import json
import regex
from pygtail import Pygtail
from SpaceAwareConfigParser import SpaceAwareConfigParser
from pg_pattern import PgPattern


def get_last_log(log_dir):
    return max(glob.iglob('%s/*.log' % log_dir), key=os.path.getctime)


def load_config(filename):
    config_dict = {}
    config = SpaceAwareConfigParser()
    config.read(filename)
    config_dict['redis_ip']     = config.get('main',    'redis_ip')
    config_dict['redis_port']   = config.getint('main', 'redis_port')
    config_dict['pg_log_dir']   = config.get('main',    'pg_log_dir')
    config_dict['logging']      = config.get('other',   'logging')
    return config_dict


def split_glob_msg(glob_msg):
    for match in regex.finditer(PG_PATTERN, glob_msg, flags=regex.IGNORECASE+regex.DOTALL):
        yield {
            'ip': match.group('user_ip'),
            'timestamp': glob_msg[1],
            'header': match.group('header'),
            'log_text': match.group('log_text'),
        }


if __name__ == "__main__":
    config = load_config('pg_log.conf')
    PG_PATTERN = PgPattern().from_log_format('%m %u@%d %h %c ')

    logging.basicConfig(filename=config['logging'], level=logging.DEBUG)
    rc = redis.StrictRedis(host=config['redis_ip'], port=config['redis_port'], db=0)
    filename = get_last_log(config['pg_log_dir'])
    print('init log file: %s' % filename)
    offset_file = '%s_ps.offset' % time.time()

    log_rotated_timestamp = datetime.datetime.utcnow()
    clean_tick = 0
    file_rotated = 0
    while True:
        msg_count = 0
        # открываем цикл и бесконечно читаем-пишем раз в секунду
        buf = Pygtail(filename, offset_file=offset_file).read()
        if buf:
            for msg in split_glob_msg(buf):
                rc.publish(msg['ip'], json.dumps(msg))

        time.sleep(1)

        new_filename = get_last_log(config['pg_log_dir'])
        if filename != new_filename:
            filename = new_filename
            offset_file = '%s.offset_ps' % time.time()
            print('log file rotated, new: %s' % filename)
            if (datetime.datetime.utcnow() - log_rotated_timestamp).total_seconds() < 30:
                file_rotated += 1
                if file_rotated == 2:
                    file_rotated = 0
                    print('rotations are too frequient, timeout 30s')
                    time.sleep(30)
            else:
                file_rotated = 0
            log_rotated_timestamp = datetime.datetime.utcnow()
