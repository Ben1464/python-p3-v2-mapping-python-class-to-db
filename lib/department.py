import sqlite3

# Connect to the database
CONN = sqlite3.connect('your_database.db')
CURSOR = CONN.cursor()

class Department:
    @classmethod
    def create_table(cls):
        """Creates the departments table if it does not exist."""
        sql = """
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT
        )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drops the departments table if it exists."""
        sql = "DROP TABLE IF EXISTS departments"
        CURSOR.execute(sql)
        CONN.commit()

    def __init__(self, name, location, id=None):
        self.name = name
        self.location = location
        self.id = id

    def save(self):
        """Saves the Department instance to the database."""
        if self.id is None:
            sql = "INSERT INTO departments (name, location) VALUES (?, ?)"
            CURSOR.execute(sql, (self.name, self.location))
            self.id = CURSOR.lastrowid
        else:
            sql = "UPDATE departments SET name = ?, location = ? WHERE id = ?"
            CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    @classmethod
    def create(cls, name, location):
        """Creates a new row in the departments table and returns a Department instance."""
        instance = cls(name, location)
        instance.save()
        return instance

    def update(self):
        """Updates the instance's corresponding row in the database."""
        sql = "UPDATE departments SET name = ?, location = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        """Deletes the instance's corresponding row from the database."""
        sql = "DELETE FROM departments WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
