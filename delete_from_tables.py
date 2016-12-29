#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'db_user',
    'password': 'db_password',
    'host': '127.0.0.1',
    'port': '3306',
    'database': 'db'
}

cnx = cur = None
try:
    cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Something is wrong with your user name or password')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    reply = str(raw_input('Would you like to make tables empty? [Y/N, Default:Y]')).strip()
    if len(reply)==0 or reply[0].lower() in ['y', 'yes']:
        cur = cnx.cursor()
        cur.execute('SET FOREIGN_KEY_CHECKS = 0;')
        cur.execute('SET AUTOCOMMIT = 0;')
        cur.execute('START TRANSACTION;')
        cur.execute('SHOW TABLES;')
        for row in cur.fetchall():
            table = ''.join(row)
            command = 'DELETE FROM ' + table + ';'
            cur.execute(command)
            print(command)

        cur.execute('SET FOREIGN_KEY_CHECKS = 1;')
        cur.execute('SET AUTOCOMMIT = 1;')
        cnx.commit()
    else:
        print('Bye!')
finally:
    if cur:
        cur.close()
    if cnx:
        cnx.close()
