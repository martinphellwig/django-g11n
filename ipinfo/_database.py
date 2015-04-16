"""
Using a sqlite database for fast lookup.
"""
import csv
import sqlite3
import ipaddress
import socket
import binascii

from _ip2country import write_csv

DBN = 'ipdb.sq3'

class Database(object):
    "Database abstraction."
    def __init__(self, filename=None):
        if filename == None:
            filename = write_csv()

        table = 'ipranges'
        self.cnx = sqlite3.connect(DBN)
        self.cursor = self.cnx.cursor()
        self._create_table(table)

        with open(filename) as file_open:
            reader = csv.reader(file_open)
            next(reader) # skip header
            data = list(reader)
            self._insert_data(table, data)

    def _insert_data(self, table, data):
        "Insert data where appropiate"
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
                    row[-1] = str(row[-1])
                    row[-2] = str(row[-2])
                    inserts.append(row)

            sql = """INSERT INTO ipranges(rid, nic, tldcc, ip_version,
                                          network, broadcast) 
                    VALUES (?, ?, ?, ?, ?, ?)"""
            self.cursor.executemany(sql, inserts)
        else:
            print('# No new records found.')
        self.cnx.commit()

    def _has_table(self, name):
        "Do we have the table in the database"
        meta = self.cursor.execute("PRAGMA table_info('%s')" % name)
        return len(meta.fetchall()) > 0

    def _create_table(self, name):
        "Create table"
        if self._has_table(name):
            return
        sql = """
        CREATE TABLE %s
            (rid         TEXT,
             nic         TEXT,
             tldcc       TEXT,
             ip_version  INTEGER,
             network     BLOB,
             broadcast   BLOB)
        """ % name

        self.cursor.execute(sql)

    def get_record(self, address):
        "Get the record from the database"
        address = ipaddress.ip_address(address)

        if address.version == 4:
            _af = socket.AF_INET
        else:
            _af = socket.AF_INET6

        packed_string = socket.inet_pton(_af, address.exploded)
        integer = int(binascii.hexlify(packed_string), 16)

        sql = """
        SELECT * FROM ipranges WHERE
                network < ? 
            AND broadcast > ?
            AND LENGTH(network) <= ?
            AND LENGTH(broadcast) >= ?"""
        item = str(integer)
        length = len(item)

        self.cursor.execute(sql, [item, item, length, length])
        return self.cursor.fetchall()

    def return_tldcc(self, address):
        "Just return the country code"
        # it is actually TLDcc which can also include regions like EU
        return self.get_record(address)[0][2]

if __name__ == '__main__':
    database = Database('/tmp/ip_country_range_2015_04_16T11_42_35_001479.csv')
    print(database.return_tldcc('221.192.143.171'))
    

        
        