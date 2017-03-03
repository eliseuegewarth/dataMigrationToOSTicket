# -*- coding: utf-8 -*-
import csv
import sys
from datetime import date, datetime
import mysql.connector

def main(argv):
    import_organization_from_csv(argv)

def import_organization_from_csv(filename):
    ## Do not run the command below in production ##
    # truncate()

    cnx = mysql.connector.connect(user='osticket', password='secret', database='osticket', host='127.0.0.1', port='3306')
    cursor = cnx.cursor()

    add_user = ("INSERT INTO ost_user "
                        "(name, created, updated) "
                        "VALUES (%(name)s, %(created)s, %(updated)s)"
                        )
    id_position = 0
    user_name_position = 1

    now = datetime.now().date()
    
    #  ## change to open csv id map ## with open(filename) as csvfile:
    with open(filename) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        first = True
        for row in spamreader:
            if not first:
                data_user = {
                    'name': row[user_name_position],
                    'created': now,
                    'updated': now,
                }
                cursor.execute(add_user, data_user)
                last_user = cursor.lastrowid
                csv_template_string = '"{0}","{1}"'.format(row[id_position] , last_user)
                print (csv_template_string)
                
            else:
                first = False

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()

def truncate():
    cnx = mysql.connector.connect(user='osticket', password='secret', database='osticket', host='127.0.0.1', port='3306')
    cursor = cnx.cursor()
    query = """truncate table ost_user""" 
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

if __name__ == "__main__":
   main(sys.argv[1])
