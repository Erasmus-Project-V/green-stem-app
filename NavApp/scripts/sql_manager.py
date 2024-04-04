from sqlite3 import connect
import os

SQL_BASE_NAME = "activities.db"


class SQLManager:

    def __init__(self, user_id):
        self.in_writing = False
        self.has_new = False
        self.user_id = user_id
        has_file = SQL_BASE_NAME in os.listdir()
        self.connection = connect(SQL_BASE_NAME)
        self.cursor = self.connection.cursor()
        if not has_file:
            self.__build_base()
        else:
            self.__check_empty()

    def __check_empty(self):
        command = "SELECT * FROM exercises"
        fd = self.cursor.execute(command).fetchall()
        if fd:
            self.has_new = True
    def __create_table(self, table_name, table_vars):
        command = f"CREATE TABLE {table_name} ("
        for ts, tp in table_vars:
            command += f"{ts} {tp},"
        command = command[:-1] + ")"
        self.cursor.execute(command)

    def __build_base(self):
        self.__create_table("exercises", [
            ("type", "TEXT"), ("user", "TEXT"), ("time_started", "TEXT"),
            ("time_elapsed", "REAL"), ("total_distance", "INTEGER"), ("average_velocity", "INTEGER")
        ])
        ## upitno
        self.__create_table("locations", [
            ("user", "TEXT"), ("exercise", "TEXT"), ("latitude", "BLOB"),
            ("longitude", "BLOB"), ("velocity", "BLOB"), ("distance", "BLOB")
        ])

    def __insert_into_table(self, table_name, values):
        command = f"INSERT INTO {table_name} VALUES ({'?,' * len(values)}"[:-1] + ")"
        print(command)
        self.cursor.execute(command, tuple(values))

    def __destroy_base(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
        os.remove(SQL_BASE_NAME)

    def add_finished_activity(self, exercise, location_data):
        self.in_writing = True
        self.__insert_into_table("exercises", exercise.values())
        print(location_data)
        self.__insert_into_table("locations", location_data.values())
        self.connection.commit()
        self.in_writing = False
        self.has_new = True

    def fetch_all(self):
        command1 = "SELECT * FROM exercises"
        command2 = "SELECT * FROM locations"
        de = self.cursor.execute(command1).fetchall()
        dl = self.cursor.execute(command2).fetchall()
        if not de:
            de, dl = [], []
        return de, dl

    def clear_base(self):
        self.has_new = False
        command1 = "DELETE FROM exercises"
        command2 = "DELETE FROM locations"
        self.cursor.execute(command1)
        self.cursor.execute(command2)
        self.connection.commit()

