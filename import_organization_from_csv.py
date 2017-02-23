# -*- coding: utf-8 -*-
import csv
import sys

import mysql.connector

def main(argv):
    import_organization_from_csv(argv)

def import_organization_from_csv(filename):

    # cnx = mysql.connector.connect(user='osticket', password='secret', database='osticket', host='127.0.0.1', port='3306')
    # cursor = cnx.cursor()

    add_organization = ("INSERT INTO ost_organization "
                        "(name, extra) "
                        "VALUES (%(name)s, %(extra)s)"
                        )
    id_position = 0
    org_name_position = 1

    with open(filename) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        first = True
        for row in spamreader:
            if not first:
                data_organization = {
                    'name': row[org_name_position],
                    'extra': row[id_position]
                    }
                # cursor.execute(add_organization, data_organization)
                print (add_organization % data_organization)
                
            else:
                first = False

    # Make sure data is committed to the database
    # cnx.commit()

    # cursor.close()
    # cnx.close()


if __name__ == "__main__":
   main(sys.argv[1])
