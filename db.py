import mysql.connector
def connect():

    db = mysql.connector.connect(
    host="gkchef69.mysql.pythonanywhere-services.com",
    user="gkchef69",
    passwd="giorgos1711",
    database="gkchef69$recipes",
    autocommit=True,
    port = 3306
    )


    cursor = db.cursor()

    return db, cursor

def create_user(username, password):
    db, cursor = connect()


    sql = 'INSERT INTO `users` (username, password) VALUES (%s, %s)'
    vals = (username, password)

    cursor.execute(sql, vals)

def remove_user(id_or_name):
    db, c = connect()

    if not len(id_or_name) > 2:

        id_or_name = int(id_or_name)

    sql = 'DELETE FROM `users` WHERE username = %s OR id = %s'
    val = (id_or_name, id_or_name)

    c.execute(sql, val)
    db.commit()

    print("user removed successfully")

    # Additional code if needed

def print_users():
    db, c = connect()

    sql = 'SELECT * FROM `users`'

    c.execute(sql)

    print(c.fetchall())


if __name__ == '__main__':
    db, c = connect()

    while True:

        e = input("what do you want to do (add/remove/show/quit) : ")

        if e.lower() == 'add':


            while True:
                try:
                    name = input('enter user username: ')
                    if len(name) < 3:
                        raise Exception("USERNAME MUST BE ATLEAST 3 LETTERS")
                    sql = 'SELECT * FROM `users`'
                    c.execute(sql)

                    fet = c.fetchall()

                    for user in fet:

                        if user[1] == name:

                            raise Exception("Αυτο το username υπαρχει")



                    password = input('enter user password: ')

                    create_user(name , password)
                    print(f"created user '{name}' with password '{password}' successfully!")
                    break
                except Exception as e:

                    print("\n" + str(e) + "\n")

        elif e.lower() == 'remove':

            name_or_id = input("enter name or id: ")

            remove_user(name_or_id)

        elif e.lower() == 'show':

            print_users()

        elif e.lower() == 'quit':

            break





