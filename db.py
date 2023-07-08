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