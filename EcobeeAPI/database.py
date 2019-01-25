import mysql.connector

class Database:

    def __init__(self, host, dbname, username, password):
        self.host = host
        self.dbname = dbname
        self.username = username
        self.password = password

        self.mydb = mysql.connector.connect(
            host=host,
            database=dbname,
            user=username,
            passwd=password
            )

    def add_temperature(self, table, date_added, sensor, indoor_temp, outside_temp):
        self.table = table
        self.date_added = date_added
        self.sensor = sensor
        self.indoor_temp = indoor_temp
        self.outside_temp = outside_temp
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO " + table + " (date_added, sensor, indoor_temp, outside_temp) VALUES (%s, %s, %s, %s)"
        val = (date_added, sensor, indoor_temp, outside_temp)
        mycursor.execute(sql, val)
        self.mydb.commit()

    def delete_item(self, table, id):
        self.id = id
        self.table = table
        mycursor = self.mydb.cursor()
        sql = "DELETE FROM {table} WHERE ID = {id}"
        val = (id, )
        print(mycursor.execute(sql, val))
        self.mydb.commit()

    def update_task(self, duedate, title, description, status):
        self.duedate = duedate
        


