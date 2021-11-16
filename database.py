class db:
    def __init__(self,database,table):
        import sqlite3
        self.conn = sqlite3.connect(database,check_same_thread=False)
        self.c = self.conn.cursor()
        self.database = database
        self.table = table
    
    def setup(self,*args):
        self.to_write = f"CREATE TABLE IF NOT EXISTS {self.table} ("
        for i in range(len(args)):
            self.to_write += f"{str(args[i])} characters(100)"
            if i != len(args)-1:
                self.to_write += ","
        self.to_write += ")"
        self.c.execute(self.to_write)
        self.conn.commit()

    def read(self):
        self.c.execute(f"SELECT * FROM {self.table}")
        self.conn.commit()
        self.lines = self.c.fetchall()
        return self.lines

    def insert(self,*args):
        self.to_write = f"INSERT INTO {self.table} VALUES ("
        for i in range(len(args)):
            self.to_write += f"\"{str(args[i])}\""
            if i != len(args)-1:
                self.to_write += ","
        self.to_write += ")"
        self.c.execute(self.to_write)
        self.conn.commit()

    def columns(self):
        self.c.execute(f"PRAGMA table_info({self.table})")
        self.conn.commit()
        self.columns_values = []
        for x in self.c.fetchall():
            self.columns_values.append(x[1])
        return self.columns_values
    
    def drop(self):
        self.c.execute(f"DROP TABLE {self.table}")
        self.conn.commit()

    def remove(self,value, column_number):
        self.to_write = f"DELETE FROM {self.table} WHERE "
        self.to_write += f"{self.columns()[column_number-1]} = '{value}'"
        self.c.execute(self.to_write)
        self.conn.commit()

    def remove_max(self,value, column_number,value2, column_number2):
        self.to_write = f"DELETE FROM {self.table} WHERE "
        self.to_write += f"{self.columns()[column_number-1]} = '{value}' AND {self.columns()[column_number2-1]} = '{value2}'"
        self.c.execute(self.to_write)
        #print(self.to_write)
        self.conn.commit()
        return self.c.fetchall()
    
    def select(self,value, column_number):
        self.to_write = f"SELECT * FROM {self.table} WHERE "
        self.to_write += f"{self.columns()[column_number-1]} = '{value}'"
        self.c.execute(self.to_write)
        #print(self.to_write)
        self.conn.commit()
        return self.c.fetchall()
    
    def select_max(self,value, column_number,value2, column_number2):
        self.to_write = f"SELECT * FROM {self.table} WHERE "
        self.to_write += f"{self.columns()[column_number-1]} = '{value}' AND {self.columns()[column_number2-1]} = '{value2}'"
        self.c.execute(self.to_write)
        #print(self.to_write)
        self.conn.commit()
        return self.c.fetchall()

    def update_max(self, condition_1, condition_1_column_number, condition_2, condition_2_column_number, value, column_number):
        self.to_write = f"UPDATE {self.table} "
        self.to_write += f"SET {self.columns()[column_number-1]} = '{value}' "
        self.to_write += f"WHERE {self.columns()[condition_1_column_number-1]} = '{condition_1}' AND {self.columns()[condition_2_column_number-1]} = '{condition_2}' "
        self.c.execute(self.to_write)
        self.conn.commit()

    def clear(self):
        self.c.execute(f"DELETE FROM {self.table}")
        self.conn.commit()
