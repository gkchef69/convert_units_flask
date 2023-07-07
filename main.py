from flask import Flask,flash ,render_template, make_response, request, redirect, url_for
import mysql.connector
import convert

app = Flask(__name__)

@app.route("/")
def root():
    return render_template('base.html')

AUTHENTICATED = False

@app.route("/login",methods=['GET','POST'])
def add_recipe():
    if request.method=='GET':
        resp = make_response(render_template('login.html'))
        return resp
    else:
        password = request.form['password']
        if password=="lessgo":
            resp = make_response(render_template('base.html'))
            resp.set_cookie('pass', "lessgo")
            return resp
        else:
            return "Incorrect password"

@app.route("/convert",methods=['GET','POST'])
def convert_web():
    items = convert.get_items()
    db = mysql.connector.connect(
    host="gkchef69.mysql.pythonanywhere-services.com",
    user="gkchef69",
    passwd="giorgos1711",
    database="gkchef69$recipes",
    autocommit=True,
    port = 3306
    )

    cursor = db.cursor()
    if request.method=='GET':
        resp = make_response(render_template('convert.html',items=items, result="", res_1="", res_2="",sep="",item=""))
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

        item += ":"
        # print("einai: " + afto)
        # i = afto.split()
        # print(i)
        starting = afto.split()[0] + FROM.replace(" ","")
        print(starting)
        print(afto)
        # seper = afto.split()[3]
        ending = f"{afto.split()[4]}{TO} {item}"
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
                req_method = request.method
        ))
        return resp
    print(res_2)
    print(res_1)

@app.route("/add_item", methods=["GET", "POST"])
def add_item_function():
    db = mysql.connector.connect(
    host="gkchef69.mysql.pythonanywhere-services.com",
    user="gkchef69",
    passwd="giorgos1711",
    database="gkchef69$recipes",
    autocommit=True,
    port = 3306
    )

    cursor = db.cursor()

    write_to_db = True

    if request.method == "GET":

        done_msg = ""
        return make_response(render_template("add_item.html",msg=done_msg))

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

        return make_response(render_template("add_item.html", msg=done_msg))

@app.route("/remove_item", methods=["GET", "POST"])
def remove_item():
    db = mysql.connector.connect(
    host="gkchef69.mysql.pythonanywhere-services.com",
    user="gkchef69",
    passwd="giorgos1711",
    database="gkchef69$recipes",
    autocommit=True,
    port = 3306
    )

    cursor = db.cursor()

    done_msg = ""

    cursor.execute("SELECT id,name FROM items")
    items = cursor.fetchall()
    print(items)

    if request.method == "GET":
        resp = make_response(render_template("delete_item.html", msg =done_msg, items=items))
        return resp

    if request.method == "POST":

        item = request.form["item"]

        cursor.execute("SELECT id,name FROM items")
        items = cursor.fetchall()

        sql = "DELETE FROM items WHERE name=%s"

        cursor.execute(sql, (item,))
        db.commit()

        done_msg = f"Removed item from database '{item}'"
        return make_response(render_template("delete_item.html", msg=done_msg, items = items))

items = {}

@app.route("/search_item", methods=["GET", "POST"])
def search_item():
    db = mysql.connector.connect(
    host="gkchef69.mysql.pythonanywhere-services.com",
    user="gkchef69",
    passwd="giorgos1711",
    database="gkchef69$recipes",
    autocommit=True,
    port = 3306
    )

    cursor = db.cursor()

    if request.method=="GET":

        cursor.execute("SELECT * FROM items")
        item_list = cursor.fetchall()
        print(item_list)
        return make_response(render_template("search_item.html", items=item_list))


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
    db = mysql.connector.connect(
    host="gkchef69.mysql.pythonanywhere-services.com",
    user="gkchef69",
    passwd="giorgos1711",
    database="gkchef69$recipes",
    autocommit=True,
    port = 3306
    )

    cursor = db.cursor()
    if request.method == "GET":
        print("get")
        return make_response(render_template("update_item.html", stuff = items))


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

        delete_sql = "DELETE FROM `items` WHERE `id` = %s"
        delete_val = (id,)
        cursor.execute(delete_sql, delete_val)

        insert_sql = "INSERT INTO `items` (`id`, `name`, `kg`, `grams`, `cups`, `liter`, `oz`, `tbsp`, `tsp`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert_val = (id, name, kg, grams, cups, liter, oz, tbsp, tsp)
        cursor.execute(insert_sql, insert_val)

        db.commit()

        return redirect(url_for('search_item'))
        # return make_response(render_template("update_item.html", stuff = items))


db = mysql.connector.connect(
    host="gkchef69.mysql.pythonanywhere-services.com",
    user="gkchef69",
    passwd="giorgos1711",
    database="gkchef69$recipes",
    autocommit=True,
    port = 3306
    )

cursor = db.cursor()

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

