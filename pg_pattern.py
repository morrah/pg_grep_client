#!/usr/bin/env python
# -*- coding: utf-8 -*-
import regex

class PgPattern(object):
    FORMAT_PATTERNS = {
        #'%a': u'(?P<app_name>[a-z0-9_]*)', # Application name
        '%u': u'(?P<user_name>[a-zA-Z0-9_\.-]*)', # User name
        '%d': u'(?P<db_name>[a-zA-Z0-9_]*)', # Database name
        #'%r': u'(\d{1,3}(?:\.\d{1,3}){3}:[0-9]{1,5}|\[local\]:[0-9]{1,5})', # Remote host name or IP address, and remote port
        '%h': u'(?P<user_ip>\d{1,3}(?:\.\d{1,3}){3}|\[local\])', # Remote host name or IP address
        #'%p': u'([a-f0-9]+)', # Process ID
        #'%t': u'(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d\ ([A-Z]+|\+\d\d\d))', # Time stamp without milliseconds
        '%m': u'(?P<timestamp>\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d\.\d+ ([A-Z]+|\+\d\d\d))', # Time stamp with milliseconds
        #'%i': u'([a-z0-9_]*)', # Command tag: type of session's current command
        #'%e': u'([a-z0-9_]*)', # SQLSTATE error code
        '%c': u'(?P<session_id>[a-f0-9]+\.[a-f0-9]+)', # Session ID
        #'%l': u'([a-z0-9_]*)', # Number of the log line for each session or process, starting at 1
        #'%s': u'([a-z0-9_]*)', # Process start time stamp
        #'%v': u'([a-z0-9_]*)', # Virtual transaction ID (backendID/localXID)
        #'%x': u'([a-z0-9_]*)', # Transaction ID (0 if none is assigned)
        #'%q': u'([a-z0-9_]*)', # Produces no output, but tells non-session processes to stop at this point in the string; ignored by session processes
        '%%': u'%', # Literal %
    }

    LOG_LEVEL = (
        u'ОТМЕТКА',
        u'ПОДРОБНОСТИ',
        u'ПОЛОЖЕНИЕ',
        u'ПОДСКАЗКА',
        u'ПРЕДУПРЕЖДЕНИЕ',
        u'СБОЙ',
        u'ОШИБКА',
        u'ОПЕРАТОР',
        u'СООБЩЕНИЕ',
    )

    def from_log_format(self, log_format):
        # replace every literal by regexp from FORMAT_PATTERNS
        log_format_list = self._compile_pattern(log_format)
        pattern = ''
        for el in log_format_list:
            if self.FORMAT_PATTERNS.get(el):
                pattern += self.FORMAT_PATTERNS.get(el)
            else:
                pattern += el
        pattern += '(%s)' % u'|'.join( ['%s:' % l for l in self.LOG_LEVEL] )
        pattern  = '(?V1)(?<header>(%s))' % pattern
        # match log_text until new log-messsage starts (recursive group) or end of string
        pattern += ' (?P<log_text>.*?)(?=(?&header)|$)'
        return pattern

    # split log_format to list of literals
    def _compile_pattern(self, log_format, level=0):
        for key in self.FORMAT_PATTERNS.keys():
            if key in log_format:
                (left,right) = log_format.split(key)
                center = key
                left_res = self._compile_pattern(left,level+1)
                right_res = self._compile_pattern(right,level+1)
                return left_res + [center] + right_res
        return [log_format]

if __name__ == '__main__':
    test_log_format = '%m %u@%d %h %c '
    test_string = u'2016-02-25 19:22:57.328 MSK postgres@Razgon 10.10.10.202 56cf0e2c.1c96 ОТМЕТКА:  продолжительность: 0.086 мс\n2016-02-25 19:22:57.328 MSK postgres@Razgon 10.10.10.202 56cf0e2c.1c96 ОТМЕТКА:  оператор: EXECUTE qpsqlpstmt_1c62 (3, 3, 11)\n2016-02-25 19:22:57.328 MSK postgres@Razgon 10.10.10.202 56cf0e2c.1c96 ПОДРОБНОСТИ:  подготовка: PREPARE qpsqlpstmt_1c62 AS update ststatus  set fstatus = $1, fsubstatus=$2, datestatus=now()  where id = $3\n2016-02-25 19:22:57.329 MSK postgres@Razgon 10.10.10.202 56cf0e2c.1c96 ОТМЕТКА:  продолжительность: 0.455 мс\n2016-02-25 19:22:57.329 MSK postgres@Razgon 10.10.10.202 56cf0e2c.1c96 ОТМЕТКА:  оператор: PREPARE qpsqlpstmt_1c63 AS insert into agdataexchage (dateexchange,idobject,typerequest,data,idparent,freeMem,cpuIdle,uptime)values (current_timestamp,$1,$2,$3,$4,$5,$6,$7)\n'

    pattern = PgPattern().from_log_format(test_log_format)
    for match in regex.finditer(pattern, test_string, flags=regex.IGNORECASE+regex.DOTALL):
        print(match.group('timestamp'), match.group('log_text')) # match.group('user_name'), match.group('db_name'), match.group('user_ip'), match.group('session_id')
