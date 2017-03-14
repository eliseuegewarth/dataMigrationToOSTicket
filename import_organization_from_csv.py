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

    add_organization = ("INSERT INTO ost_organization "
                        "(name, created, updated) "
                        "VALUES (%(name)s, %(created)s, %(updated)s)"
                        )
    id_position = 0
    org_name_position = 1
    
    now  = datetime.now().date()
    organization_map = open('organizacoes_map.csv', 'w')
    csv_template_string = "{0},{1}".format('"sigi_id"' , '"OSTicket_id"')
    print (csv_template_string, end="\n", file=organization_map)

    with open(filename) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        first = True
        for row in spamreader:
            if not first:
                data_organization = {
                    'name': row[org_name_position],
                    'created': now,
                    'updated': now,
                    }
                cursor.execute(add_organization, data_organization)
                last_organization = cursor.lastrowid
                csv_template_string = '"{0}","{1}"'.format(row[id_position] , last_organization)
                print (csv_template_string, end="\n", file=organization_map)
                
            else:
                first = False

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()

def truncate():
    cnx = mysql.connector.connect(user='osticket', password='secret', database='osticket', host='127.0.0.1', port='3306')
    cursor = cnx.cursor()
    query = """truncate table ost_organization""" 
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

if __name__ == "__main__":
   main(sys.argv[1])
