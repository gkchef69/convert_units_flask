from fractions import Fraction
import mysql.connector
import db as dba

db, c = dba.connect()

def get_items():
    db, c = dba.connect()
    c.execute("SELECT `name` FROM items")
    return c.fetchall()

def convert(quantity,item, fromwhat, towhat):
    db, c = dba.connect()
    sql = """SELECT * FROM `items` WHERE name = %s"""

    c.execute(sql,([item]))

    return_fraction = False

    my_item = c.fetchone()
    print(my_item)
    fromwhat,towhat = fromwhat.lower(),towhat.lower()
    if fromwhat == "kg":
        val_1 = my_item[2]

    if fromwhat == "gram":
        val_1 = my_item[3]

    if fromwhat == "cups":
        val_1 = my_item[4]

    if fromwhat == "liter":
        val_1 = my_item[5]

    if fromwhat == "oz":
        val_1 = my_item[6]

    if fromwhat == "tbsp":
        val_1 = my_item[7]

    if fromwhat == "tsp":
        val_1 = my_item[8]

    amount =quantity

    print(my_item)
    if towhat == "kg":
        val_2 = my_item[2]

    if towhat == "gram":
        val_2 = my_item[3]


    if towhat == "cups":
        val_2 = my_item[4]
        return_fraction = True

    if towhat == "liter":
        val_2 = my_item[5]

    if towhat == "oz":
        val_2 = my_item[6]

    if towhat == "tbsp":
        val_2 = my_item[7]
        return_fraction = True

    if towhat == "tsp":
        val_2 = my_item[8]
        return_fraction = True
    print (f" >>  {val_2}")
    print (f" >  {val_1}")
    difference = val_2/val_1

    value = float(amount) * difference

    if return_fraction:

        string = str(round(value,3))

        string  = string.split(".")
        # print(f"pio {string}")
        first_part = string[0]

        string = float("0." + string[1])

        # print(f"string = {string}")

        if string >= 0.6:
            string = 0.75

        elif string > 0.37:
            string = 0.5

        elif string > 0.10:
            string = 0.25

        else:
            string = 0
        # print(f"{string}  einai {string}")
        if string == 0:
            plus = ""
            fraction = ""
        elif string < 1:
            if towhat == "cups":
                plus = "&"
                first_part = ""
                # print(f"{string}  einai22 {string}")
                # print(type(string))
            # string = str(string)
            # print(f"{string}  einai333 {string}")
            # print(type(string))
            else:
                plus = "&"
                # string = split[0:]
                # first_part = ""
            fraction = Fraction(string)
        else:
            plus = "&"
            fraction = Fraction(string)
        print(type(first_part), fraction)
        # print(towhat)
        return {'amount' : amount, "fromwhat" : fromwhat, "item" : item, "result" : str(int(value)) + plus + str(fraction), "towhat" : towhat, "item" : item}

    return {'amount' : amount, "fromwhat" : fromwhat, "item" : item, "result" : f"{round(value, 3)}", "towhat" : towhat, "item" : item}

