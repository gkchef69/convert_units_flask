from flask import Flask,flash ,render_template, make_response, request, redirect, url_for
import mysql.connector
import convert
import db as dba

app = Flask(__name__)

sesh = {'authenticated' : False}

@app.route("/")
def root():
    db, cursor = dba.connect()

    # if not sesh["authenticated"]:

    #     return redirect(url_for('login'))


    return render_template('base.html', sesh = sesh)

@app.route('/logout')
def logout():

    sesh["authenticated"] = False

    return redirect(url_for('root'))



@app.route("/login",methods=['GET','POST'])
def login():
    db, cursor = dba.connect()


    if request.method == 'POST':

        sql  = 'SELECT * FROM `users`'
        cursor.execute(sql)

        for user in cursor.fetchall():

            if user[1] == request.form.get('username') and user[2] == request.form.get('password'):

                sesh["authenticated"] = True


                return redirect(url_for('root'))


    return render_template('login.html', sesh = sesh)


    # if request.method=='GET':
    #     resp = make_response(render_template('login.html'))
    #     return resp
    # else:
    #     password = request.form['password']
    #     if password=="lessgo":
    #         resp = make_response(render_template('base.html'))
    #         resp.set_cookie('pass', "lessgo")
    #         return resp
    #     else:
    #         return "Incorrect password"

@app.route("/convert",methods=['GET','POST'])
def convert_web():

    db, cursor = dba.connect()

    items = convert.get_items()
    if request.method=='GET':
        resp = make_response(render_template('convert.html',items=items, result="", res_1="", res_2="",sep="",item="", sesh = sesh))
        return resp
    if request.method=='POST':

        item = request.form['item']
        item.replace(" ", "")
        print(item)

        FROM = request.form['from']
        TO = request.form['to']

        # print(FROM)
        # print(TO)

        # print(f"FROM : {FROM} \nTO {TO}")

        afto = convert.convert(
            request.form['amount'],item,FROM,TO
            )

        # item += ":"
        # # print("einai: " + afto)
        # # i = afto.split()
        # # print(i)
        # starting = afto.split()[0] + FROM.replace(" ","")
        starting = 'no'
        # print(starting)
        # print(afto)
        # # seper = afto.split()[3]
        # ending = f"{afto.split()[4]}{TO} {item}"
        ending = 'yes'




        separator = "Είναι: "
        # print(afto.split()[0])
        # print(afto)

        resp = make_response(render_template('convert.html',
                items=items,
                result=afto,
                res_1=starting,
                res_2=ending,
                sep=separator,
                item=item,
                req_method = request.method,

                dict = afto,
                sesh = sesh
        ))
        return resp
    # print(res_2)
    # print(res_1)

@app.route("/add_item", methods=["GET", "POST"])
def add_item_function():
    if not sesh["authenticated"]:

        return redirect(url_for('login'))

    db, cursor = dba.connect()

    write_to_db = True

    if request.method == "GET":

        done_msg = ""
        return make_response(render_template("add_item.html",msg=done_msg, sesh = sesh))

    if request.method == "POST":

        name = request.form["name"]
        kg = request.form["kg"]
        oz = request.form["oz"]
        grams = request.form["grams"]
        cups = request.form["cups"]
        liter = request.form["liters"]
        tbsp = request.form["tbsp"]
        tsp = request.form["tsp"]

        sql = "INSERT INTO items (name, kg, grams, cups, oz, liter, tbsp, tsp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (name, kg, grams, cups, oz, liter, tbsp, tsp)

        done_msg = f"Succesfully added {name} to database"

        try:
            cursor.execute(sql, val)
            db.commit()
        except mysql.connector.errors.IntegrityError:
            done_msg = f"Εισαι πολυ ηλιθιος, το εχεις βαλει ηδη"

        return make_response(render_template("add_item.html", msg=done_msg, sesh = sesh))

@app.route("/remove_item", methods=["GET", "POST"])
def remove_item():
    if not sesh["authenticated"]:

        return redirect(url_for('login'))

    db, cursor = dba.connect()

    done_msg = ""

    cursor.execute("SELECT id,name FROM items")
    items = cursor.fetchall()
    print(items)

    if request.method == "GET":
        resp = make_response(render_template("delete_item.html", msg =done_msg, items=items, sesh = sesh))
        return resp

    if request.method == "POST":

        item = request.form["item"]

        cursor.execute("SELECT id,name FROM items")
        items = cursor.fetchall()

        sql = "DELETE FROM items WHERE name=%s"

        cursor.execute(sql, (item,))
        db.commit()

        done_msg = f"Removed item from database '{item}'"
        return make_response(render_template("delete_item.html", msg=done_msg, items = items, sesh = sesh))

items = {}

@app.route("/search_item", methods=["GET", "POST"])
def search_item():
    if not sesh["authenticated"]:

        return redirect(url_for('login'))

    db, cursor = dba.connect()

    if request.method=="GET":

        cursor.execute("SELECT * FROM items")
        item_list = cursor.fetchall()
        print(item_list)
        return make_response(render_template("search_item.html", items=item_list, sesh = sesh))


    if request.method == "POST":
       print("aaaaaaaa")
       name = request.form["item"]

       cursor.execute("SELECT * FROM items WHERE name=%s", (name,))
       thing = cursor.fetchone()
       print(thing)
       stuff = ["id","name", "kg", "grams", "cups", "liters", "oz", "tbsp", "tsp"]


       for num,item in enumerate(stuff):
           items[item] = thing[num]


       print(items)
       return redirect(url_for("update_item"))
       #return make_response(render_template("update_item.html", stuff = items))

@app.route("/update_item", methods=["GET", "POST"])
def update_item():
    if not sesh["authenticated"]:

        return redirect(url_for('login'))


    db, cursor = dba.connect()
    if request.method == "GET":
        print("get")
        return make_response(render_template("update_item.html", stuff = items, sesh = sesh))


    if request.method == "POST":
        print("test")

        id = request.form["id"]
        name = request.form["name"]
        kg = request.form["kg"]
        oz = request.form["oz"]
        grams = request.form["grams"]
        cups = request.form["cups"]
        liter = request.form["liters"]
        tbsp = request.form["tbsp"]
        tsp = request.form["tsp"]

        # sql = "UPDATE `recipes`.`items` SET `name` = %s, `kg` = %s, `grams` = %s, `cups` = %s, `liter` = %s, `oz` = %s, `tbsp` = %s, `tsp` = %s WHERE (`id` = %s)"
        # val = (name, kg, oz, grams, cups, liter, tbsp, tsp, id)

        val_insert = (id, name, kg, grams, cups, liter, oz, tbsp, tsp)
        val_delete = (id,)

        delete_sql = "DELETE FROM `items` WHERE `id` = %s"
        cursor.execute(delete_sql, val_delete)

        insert_sql = "INSERT INTO `items` (`id`, `name`, `kg`, `grams`, `cups`, `liter`, `oz`, `tbsp`, `tsp`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_sql, val_insert)


        # cursor.execute(sql, val)
        db.commit()

        return redirect(url_for('search_item'))
        # return make_response(render_template("update_item.html", stuff = items))


db, cursor = dba.connect()

cursor.execute("""CREATE TABLE IF NOT EXISTS `recipes` (
    `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` varchar(255) NOT NULL) """)

cursor.execute("""CREATE TABLE IF NOT EXISTS `ingredients` (
    `recipe_id` INT NOT NULL,
    `ingredient` varchar(255) NOT NULL,
    `quantity` varchar(255) NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id)) """)

#    `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
#
cursor.execute("""CREATE TABLE IF NOT EXISTS `items` (
    `id` INT(10) AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(50) NOT NULL UNIQUE,
    `kg` FLOAT NOT NULL,
    `grams` FLOAT NOT NULL,
    `cups` FLOAT NOT NULL,
    `liter` FLOAT NOT NULL,
    `oz` FLOAT NOT NULL,
    `tbsp` FLOAT NOT NULL,
    `tsp` FLOAT NOT NULL
    )
     """)

cursor.execute("""CREATE TABLE IF NOT EXISTS `users` (
    `id` INT(10) AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `password` VARCHAR(50) NOT NULL
    )
     """)

# app.run(False)