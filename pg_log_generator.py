#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import random

log_lines = (
    r'2013-07-25 08:15:06.5 MSK username@servername 10.10.10.10 abf4.abf4fbaf ПОЛОЖЕНИЕ: pq_recvbuf, .\src\backend\libpq\pqcomm.c:831', 
    r'2013-07-25 08:15:06.5 MSK username@servername 10.10.10.10 abf4.abf4fbaf ОТМЕТКА: 08P01: неожиданный обрыв соединения с клиентом', 
    r'2013-07-25 08:15:06.5 MSK username@servername 10.10.10.101 abf4.abf4fbaf ПОЛОЖЕНИЕ: SocketBackend, .\src\backend\tcop\postgres.c:349', 
    r'2013-07-25 09:15:06.5 MSK username@servername 10.10.10.23 abf4.abf4fbaf ОТМЕТКА: XX000: не удалось получить данные от клиента: No connection could be made because the target machine actively refused it.', 
    r'2013-07-25 09:15:06.5 MSK username@servername 10.10.10.15 abf4.abf4fbaf ПОЛОЖЕНИЕ: pq_recvbuf, .\src\backend\libpq\pqcomm.c:831', 
    r'2013-07-25 09:15:06.5 MSK username@servername 10.10.10.15 abf4.abf4fbaf ОТМЕТКА: 08P01: неожиданный обрыв соединения с клиентом', 
    r'2013-07-25 09:15:06.5 MSK username@servername 10.10.10.15 abf4.abf4fbaf ПОЛОЖЕНИЕ: SocketBackend, .\src\backend\tcop\postgres.c:349', 
    r'2013-07-25 10:15:06.5 MSK username@servername 10.10.10.23 abf4.abf4fbaf ОТМЕТКА: XX000: не удалось получить данные от клиента: No connection could be made because the target machine actively refused it.', 
    r'2013-07-25 10:15:06.5 MSK username@servername 10.10.10.10 abf4.abf4fbaf ПОЛОЖЕНИЕ: pq_recvbuf, .\src\backend\libpq\pqcomm.c:831', 
    r'2013-07-25 10:15:06.5 MSK username@servername 10.10.10.10 abf4.abf4fbaf ОТМЕТКА: 08P01: неожиданный обрыв соединения с клиентом', 
    r'2013-07-25 10:15:06.5 MSK username@servername 10.10.10.101 abf4.abf4fbaf ПОЛОЖЕНИЕ: SocketBackend, .\src\backend\tcop\postgres.c:349', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.10 abf4.abf4fbaf ОТМЕТКА: 00000: процесс сервера (PID 5644) завершился с кодом выхода 0', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.10 abf4.abf4fbaf ПОЛОЖЕНИЕ: LogChildExit, .\src\backend\postmaster\postmaster.c:2867', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.101 abf4.abf4fbaf ОТМЕТКА: 00000: завершение всех остальных активных серверных процессов', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.23 abf4.abf4fbaf ПОЛОЖЕНИЕ: HandleChildCrash, .\src\backend\postmaster\postmaster.c:2701', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.10 abf4.abf4fbaf ПРЕДУПРЕЖДЕНИЕ: 57P02: закрытие подключения из-за краха другого серверного процесса', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.10 abf4.abf4fbaf ПОДРОБНОСТИ: Управляющий процесс отдал команду этому серверному процессу откатить текущую транзакцию и завершиться, так как другой серверный процесс завершился аварийно и возможно разрушил разделяемую память.', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.15 abf4.abf4fbaf ПОДСКАЗКА: Вы сможете переподключиться к базе данных и повторить вашу команду сию минуту.', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.10 abf4.abf4fbaf ПОЛОЖЕНИЕ: quickdie, .\src\backend\tcop\postgres.c:2592', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.23 abf4.abf4fbaf ПРЕДУПРЕЖДЕНИЕ: 57P02: закрытие подключения из-за краха другого серверного процесса', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.10 abf4.abf4fbaf ПОДРОБНОСТИ: Управляющий процесс отдал команду этому серверному процессу откатить текущую транзакцию и завершиться, так как другой серверный процесс завершился аварийно и возможно разрушил разделяемую память.', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.15 abf4.abf4fbaf ПОДСКАЗКА: Вы сможете переподключиться к базе данных и повторить вашу команду сию минуту.', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.101 abf4.abf4fbaf ПОЛОЖЕНИЕ: quickdie, .\src\backend\tcop\postgres.c:2592', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.101 abf4.abf4fbaf ПРЕДУПРЕЖДЕНИЕ: 57P02: закрытие подключения из-за краха другого серверного процесса', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.23 abf4.abf4fbaf ПОДРОБНОСТИ: Управляющий процесс отдал команду этому серверному процессу откатить текущую транзакцию и завершиться, так как другой серверный процесс завершился аварийно и возможно разрушил разделяемую память.', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.15 abf4.abf4fbaf ПОДСКАЗКА: Вы сможете переподключиться к базе данных и повторить вашу команду сию минуту.', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.101 abf4.abf4fbaf ПОЛОЖЕНИЕ: quickdie, .\src\backend\tcop\postgres.c:2592', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.101 abf4.abf4fbaf ПРЕДУПРЕЖДЕНИЕ: 57P02: закрытие подключения из-за краха другого серверного процесса', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.15 abf4.abf4fbaf ПОДРОБНОСТИ: Управляющий процесс отдал команду этому серверному процессу откатить текущую транзакцию и завершиться, так как другой серверный процесс завершился аварийно и возможно разрушил разделяемую память.', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.15 abf4.abf4fbaf ПОДСКАЗКА: Вы сможете переподключиться к базе данных и повторить вашу команду сию минуту.', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.15 abf4.abf4fbaf ПОЛОЖЕНИЕ: quickdie, .\src\backend\tcop\postgres.c:2592', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.23 abf4.abf4fbaf ОТМЕТКА: 00000: все серверные процессы завершены... переинициализация', 
    r'2013-07-25 10:47:39.5 MSK username@servername 10.10.10.15 abf4.abf4fbaf ПОЛОЖЕНИЕ: PostmasterStateMachine, .\src\backend\postmaster\postmaster.c:3122', 
    r'2013-07-25 10:47:49.5 MSK username@servername 10.10.10.101 abf4.abf4fbaf СБОЙ: XX000: ранее созданный блок разделяемой памяти всё ещё используется', 
    r'2013-07-25 10:47:49.5 MSK username@servername 10.10.10.101 abf4.abf4fbaf ПОДСКАЗКА: Если по-прежнему работают какие-то старые серверные процессы, снимите их.', 
    r'2013-07-25 10:47:49.5 MSK username@servername 10.10.10.10 abf4.abf4fbaf ПОЛОЖЕНИЕ: PGSharedMemoryCreate, .\src\backend\port\win32_shmem.c:194',
)

if __name__ == "__main__":
    with open('log/postgres.log', 'w') as f:
        while True:
            for cnt in range(1, random.randint(1,50)):
                f.write('%s\n' % (random.choice(log_lines)))
            f.flush()
            time.sleep(random.randint(1,2000)/1000)
