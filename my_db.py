import sqlite3


# To initialize database and user table.
def init():
    conn = sqlite3.connect('my_db.db')
    cursor = conn.cursor()
    sql_user = '''create table if not exists user(
        username text not null,
        guess int,
        time text)'''
    cursor.execute(sql_user)
    cursor.close()
    conn.close()


# To insert/select/delete records from user table.
# action = 'insert'/'select'/'delete', and params is a list.
def crud(action, params):
    conn = sqlite3.connect('my_db.db')
    cursor = conn.cursor()
    if action == 'insert':
        cursor.execute('insert into user values (?,?,?)', params)  # 4 values list
        print str(cursor.rowcount) + ' rows inserted.'
        print '---------------------------------'
        conn.commit()
    elif action == 'select':
        cursor.execute('select * from user where username = ?', params)  # 1 values list
        result = cursor.fetchall()
        print str(len(result)) + ' rows selected:'
        for i in result:
            print i
        print '---------------------------------'
    elif action == 'delete':
        cursor.execute('delete from user where username = ?', params)  # 1 values list
        print str(cursor.rowcount) + ' rows deleted.'
        print '---------------------------------'
        conn.commit()
    else:
        print 'Invalid action!'
    cursor.close()
    conn.close()


# Abandoned for now, may use later.
def update(username, number):
    conn = sqlite3.connect('my_db.db')
    cursor = conn.cursor()
    cursor.execute('''update user set guess = ?
        where username = ?''', [number, username])  # 4 values list
    print str(cursor.rowcount) + ' rows updated.'
    print '---------------------------------'
    conn.commit()
    cursor.close()
    conn.close()


# examples:
# init()
# crud('insert', ['admin', 0, '2018Nov28 18:28'])
# crud('select', ['admin'])
# crud('delete', ['admin'])
# crud('select', ['admin'])
# update('admin', 0)
# crud('select', ['admin'])
