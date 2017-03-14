# -*- coding: utf-8 -*-
import csv
import sys
import mysql.connector

def main():
    cnx = mysql.connector.connect(user='osticket', password='secret', database='osticket', host='127.0.0.1', port='3306')
    truncate_user_table(cnx)
    cnx = mysql.connector.connect(user='osticket', password='secret', database='osticket', host='127.0.0.1', port='3306')
    truncate_organization_table(cnx)
    cnx = mysql.connector.connect(user='osticket', password='secret', database='osticket', host='127.0.0.1', port='3306')
    truncate_user_email_table(cnx)

def truncate_user_table(cnx):
    cursor = cnx.cursor()
    query = """truncate table ost_user""" 
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def truncate_user_email_table(cnx):
    cursor = cnx.cursor()
    query = """truncate table ost_user_email""" 
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def truncate_organization_table(cnx):
    cursor = cnx.cursor()
    query = """truncate table ost_organization""" 
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

if __name__ == "__main__":
   main()
