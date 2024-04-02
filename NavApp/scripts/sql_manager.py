from sqlite3 import connect
import os

SQL_BASE_NAME = "activities.db"


class SQLManager:

    def __init__(self, user_id):
        self.in_writing = False
        self.user_id = user_id
        has_file = SQL_BASE_NAME in os.listdir()
        self.connection = connect(SQL_BASE_NAME)
        self.cursor = self.connection.cursor()
        if not has_file:
            self.__build_base()

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
            ("user", "TEXT"), ("exercise", "TEXT"), ("timestamp", "INTEGER"), ("latitude", "INTEGER"),
            ("longitude", "INTEGER") , ("velocity", "INTEGER"), ("distance","INTEGER")
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
        for l in location_data:
            self.__insert_into_table("locations", l.values())
        self.connection.commit()
        self.in_writing = False
    def upload_all(self):
        command = "null"

