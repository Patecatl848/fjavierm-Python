import datetime
import re
import sqlite3
from sqlite3 import Error

CONTACTS_TABLE_SQL = """ create table if not exists contacts (
    id integer primary key,
    name text not null,
    email text,
    added timestamp not null,
    modified timestamp not null
);"""


# creates a database connection to a database that resides in the memory
def create_connection():
    conn = None

    try:
        conn = sqlite3.connect(':memory:')
    except Error as e:
        print(e)

    return conn


# creates a table from sql statement
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def add_contact(conn, name, email):
    sql = 'insert into contacts (name, email, added, modified) values (?, ?, ?, ?)'
    cur = conn.cursor()
    cur.execute(sql, (name, email, datetime.datetime.now(), datetime.datetime.now()))
    conn.commit()


def modify_contact(conn, id, name, email):
    sql = 'update contacts set name = ?, email = ?, modified = ? where id = ?'
    cur = conn.cursor()
    cur.execute(sql, (name, email, datetime.datetime.now(), id))
    conn.commit()


def show_all_contacts():
    cur = conn.cursor()
    cur.execute('select * from contacts')
    rows = cur.fetchall()

    for row in rows:
        print(row)


def search_contacts(text):
    sql = 'select * from contacts where name like ? and email like ?'
    cur = conn.cursor()
    rows = cur.execute(sql, ('%' + text + '%', '%' + text + '%'))

    for row in rows:
        print(row)


def delete_contact(id):
    sql = 'delete from contacts where id = ?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()


if __name__ == '__main__':
    conn = create_connection()

    if conn is not None:
        create_table(conn, CONTACTS_TABLE_SQL)
    else:
        print('Database connection cannot be created.')

    option = -1
    while option != 6:
        print('Your contact book')
        print('What do you want to do? ')
        print('1. Insert a contact.')
        print('2. Modify an existing contact.')
        print('3. Show all contacts')
        print('4. Search.')
        print('5. Delete an existing contact.')
        print('6. Exit. Info will be lost!!!')

        option = int(input("Choose an option: "))

        if option == 1:
            user_input = re.split('[,\\s]*', input("Add contact (name,email): "))
            name, email = user_input[0], user_input[-1]
            add_contact(conn, name, email)
        elif option == 2:
            user_input = re.split('[,\\s]*', input("Update contact (id,name,email): "))
            id, name, email = int(user_input[0]), user_input[2], user_input[4]
            print(user_input)
            print(id)
            print(name)
            print(email)
            modify_contact(conn, id, name, email)
        elif option == 3:
            show_all_contacts()
        elif option == 4:
            text = input("Search text: ")
            search_contacts(text)
        elif option == 5:
            id = int(input("Delete contact: "))
            delete_contact(id)

        print('')

    if conn:
        conn.close()
