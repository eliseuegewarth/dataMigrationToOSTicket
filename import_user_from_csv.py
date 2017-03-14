# -*- coding: utf-8 -*-
import csv
import sys
from datetime import date, datetime
import mysql.connector

empty_string = ''
invalid_characters_string = '[~!#$%^&*, ()+{}":;\']+$'
no_email_error_message = 'No Email found'
existing_email_error_message = 'Email found in other record'
invalid_characters_error_message = 'Invalid character found in Email'
no_name_error_message = 'No name found'
email_swapped_message = 'Email found in field user_note and swapped'

contato_format_string = '"{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}"'

casa_legislativa_id_position = 1
user_name_position = 2
user_email_position = 4
user_note_position = 3
default_status = 0
default_email_id = 0

def main(users_csv, organization_id_csv):
    cnx = mysql.connector.connect(user='osticket', password='secret', database='osticket', host='127.0.0.1', port='3306')
    import_organization_from_csv(cnx, users_csv, organization_id_csv)

def import_organization_from_csv(cnx, users_csv, organization_id_csv):

    cnx = mysql.connector.connect(user='osticket', password='secret', database='osticket', host='127.0.0.1', port='3306')
    cursor = cnx.cursor()


    add_user = ("INSERT INTO ost_user "
                        "(name, org_id, default_email_id, status, created, updated) "
                        "VALUES (%(name)s, %(org_id)s, %(default_email_id)s, %(status)s, %(created)s, %(updated)s)"
                        )

    add_user_account = ("INSERT INTO ost_user_account "
                        "(user_id, status, timezone_id, dst) "
                        "VALUES (%(user_id)s, '0', '0', '0')"
                        )

    add_user_email = ("INSERT INTO ost_user_email "
                        "(user_id, address) "
                        "VALUES (%(user_id)s, %(address)s)"
                        )

    link_user_email_to_user = ("UPDATE ost_user "
                        "SET default_email_id='%(email_id)s'"
                        "WHERE id='%(user_id)s'"
                        )

    organization_id_map = create_organization_id_map(organization_id_csv)


    now = datetime.now().date()

    default_email_flags = 0

    with open(users_csv) as csvfile:

        csv_template_string = contato_format_string.format("id","casa_legislativa_id","nome","nota","email","cargo","funcao","setor","tempo_de_servico","ult_alteracao","sexo")
        contatos_sem_email = open('contatos_sem_email.csv', 'a+t')
        print (csv_template_string, end="\n", file=contatos_sem_email)
        contatos_emails_multiplos = open('contatos_emails_multiplos.csv', 'a+t')
        print (csv_template_string, end="\n", file=contatos_emails_multiplos)
        contatos_duplicados = open('contatos_duplicados.csv', 'a+t')
        print (csv_template_string, end="\n", file=contatos_duplicados)
        contatos_sem_nome = open('contatos_sem_nome.csv', 'a+t')
        print (csv_template_string, end="\n", file=contatos_sem_nome)
        
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        first = True

        no_inconsistency = True
        last_user = 0

        for row in spamreader:
            if not first:

                try:
                    if row[user_name_position] is empty_string:
                        raise mysql.connector.errors.IntegrityError( no_name_error_message )
                    else:
                        row[user_email_position] = validar_email(cnx, row[user_email_position], row[user_note_position])

                    data_user = {
                        'name': row[user_name_position],
                        'org_id': organization_id_map[row[casa_legislativa_id_position]],
                        'default_email_id': default_email_id,
                        'status': default_status,
                        'created': now,
                        'updated': now,
                    }
                    cursor.execute(add_user, data_user)

                    last_user = cursor.lastrowid

                    data_user_email = {
                        'user_id': last_user,
                        'address': row[user_email_position],
                    }

                    cursor.execute(add_user_email, data_user_email)

                    last_email = cursor.lastrowid

                    data_updated = {
                        'email_id': last_email,
                        'user_id': last_user
                    }

                    cursor.execute(link_user_email_to_user, data_updated)

                    data_user_account = {
                        'user_id': last_user,
                    }
                    cursor.execute(add_user_account, data_user_account)


                except mysql.connector.errors.IntegrityError as e:
                    cursor.execute("DELETE FROM ost_user WHERE id='%s'", last_user)

                    csv_template_string = contato_format_string.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10])

                    if (str(e) == no_email_error_message):
                        print (csv_template_string, end="\n", file=contatos_sem_email)
                    elif (str(e) == invalid_characters_error_message):
                        print (csv_template_string, end="\n", file=contatos_emails_multiplos)
                    elif (str(e) == no_name_error_message):
                        print (csv_template_string, end="\n", file=contatos_sem_nome)
                    elif (str(e) == existing_email_error_message):
                        print (csv_template_string, end="\n", file=contatos_duplicados)
                    else:
                        print (e)
                        sys.exit()
                    print (e)

            else:
                first = False

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()

def validar_email(cnx, user_email, user_note):
    email = user_email
    if email is empty_string:
        if ('@' in user_note ):
            # some users have your email stored in note position
            email = user_note

            print ("Email:<" + email + ">")
            print (email_swapped_message)

        else:
            raise mysql.connector.errors.IntegrityError( no_email_error_message )
    if set(invalid_characters_string).intersection(email):
        raise mysql.connector.errors.IntegrityError( invalid_characters_error_message )
    else:
        cursor = cnx.cursor()
        select_email = ("SELECT count(1) FROM ost_user_email WHERE address = '%s'"
                        )
        cursor.execute(select_email, email)

        for (count) in cursor:
            if not (count == 0):
                raise mysql.connector.errors.IntegrityError(existing_email_error_message)
    return email

def create_organization_id_map(organization_id_csv):
    #  ## change to open csv id map ##
    map_id = {}

    with open(organization_id_csv) as csvfile:

        first = True

        sigi_id = 0
        OSTicket_id = 1

        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if not first:
                map_id[row[sigi_id]] = row[OSTicket_id]
            else:
                first = False

    return map_id

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
