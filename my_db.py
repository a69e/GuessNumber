import sqlite3


# To initialize database and user table.
def init():
    conn = sqlite3.connect('my_db.db')
    cursor = conn.cursor()
    sql_user = '''create table if not exists user(
        user_id int,
        username text,
        game_played int,
        guess int)'''
    cursor.execute(sql_user)
    cursor.close()
    conn.close()


# To insert/select/delete records from user table.
# action = 'insert'/'select'/'delete', and params is a list.
def crud(action, params):
    conn = sqlite3.connect('my_db.db')
    cursor = conn.cursor()
    if action == 'insert':
        cursor.execute('insert into user values (?,?,?,?)', params)  # 4 values list
        print str(cursor.rowcount) + ' rows inserted.'
        conn.commit()
    elif action == 'select':
        cursor.execute('select * from user where username = ?', params)  # 1 values list
        result = cursor.fetchall()
        print str(len(result)) + ' rows selected:'
        for i in result:
            print i
    elif action == 'delete':
        cursor.execute('delete from user where username = ?', params)  # 1 values list
        print str(cursor.rowcount) + ' rows deleted.'
        conn.commit()
    else:
        print 'Invalid action!'
    cursor.close()
    conn.close()


# examples:
# init()
# crud('insert', [1, 'la', 2, 3])
# crud('select', ['la'])
# crud('delete', ['la'])
# crud('select', ['la'])
