import os
import csv
import sqlite3
import ipaddress
import socket
import binascii

from _ip2country import write_csv

DBN = 'ipdb.sq3'

class Database(object):
    def __init__(self, filename=None):
        if filename == None:
            filename = write_csv()

        table = 'ipranges'
        self.cnx = sqlite3.connect(DBN)
        self.cursor = self.cnx.cursor()
        self._create_table(table)
    
        with open(filename) as file_open:
            reader = csv.reader(file_open)
            for i in range(40):
                next(reader)
            data = list(reader)
            self._insert_data(table, data)
                        
    def _insert_data(self, table, data):
        rids_data = set()
        for row in data:
            rids_data.add(row[0])
            
        rids_dbir = set()
        
        sql = "SELECT rid FROM %s" % table
        for row in self.cursor.execute(sql):
            rids_dbir.add(row[0])
            
        remove_from_db = rids_dbir.difference(rids_data)
        if len(remove_from_db) > 0:
            print('# Removing old records from database.')
            params = ','.join(['?'] * len(remove_from_db))
            sql = "DELETE FROM %s WHERE rid in (%s)" % (table, params)
            self.cursor.execute(sql, list(remove_from_db))
        else:
            print('# No stale records found in database.')
        
        insert_into_db = rids_data.difference(rids_dbir)
        if len(insert_into_db) > 0:
            print('# Inserting new records in database')
            inserts = list()
            for row in data:
                if row[0] in insert_into_db:
                    inserts.append(row)
                    
            sql = """INSERT INTO ipranges(rid, nic, tldcc, ip_version, 
                                          network, broadcast) 
                    VALUES (?, ?, ?, ?, ?, ?)"""
            self.cursor.executemany(sql, inserts)
        else:
            print('# No new records found.')
        self.cnx.commit()
        
        
            
    def _has_table(self, name):
        meta = self.cursor.execute("PRAGMA table_info('%s')" % name)
        return len(meta.fetchall()) > 0    
                
    def _create_table(self, name):
        if self._has_table(name):
            return
        sql = """
        CREATE TABLE %s
            (rid         TEXT,
             nic         TEXT,
             tldcc       TEXT,
             ip_version  INTEGER,
             network     INTEGER,
             broadcast   INTEGER)
        """ % name
        
        self.cursor.execute(sql)
    
    def get_record(self, address):
        self.cursor.execute("SELECT * FROM ipranges")
        rows = self.cursor.fetchall()
        
        address = ipaddress.ip_address(address)

        if address.version == 4:
            af = socket.AF_INET
        else:
            af = socket.AF_INET6

        packed_string = socket.inet_pton(af, address.exploded)
        integer = int(binascii.hexlify(packed_string), 16)
        
        sql = "SELECT * FROM ipranges WHERE network<? AND broadcast>?"
        self.cursor.execute(sql, [integer, integer])
        return self.cursor.fetchall()
    
    def return_tldcc(self, address):
        return self.get_record(address)[0][2]
    
    
    
if __name__ == '__main__':
    database = Database()
    print(database.return_tldcc('213.158.89.3'))

        
        