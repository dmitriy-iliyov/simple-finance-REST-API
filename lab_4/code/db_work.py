import psycopg2


class DatabaseWorker:
    def __init__(self, db):
        self.db = db

    def get_db_connection(self):
        return psycopg2.connect(host="lab_4-db-1", database="database", user="admin", password="root")
        # return psycopg2.connect(host="localhost", database="database", user="admin", password="root")

    def create_tables(self):
        commands = (
            """ 
            CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR (20) NOT NULL,
                    password VARCHAR (200) NOT NULL
                    );
            """,
            """ 
            CREATE TABLE IF NOT EXISTS accounts (
                    id SERIAL PRIMARY KEY,
                    user_id INT,
                    money INT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                    );
            """,
            """ 
            CREATE TABLE IF NOT EXISTS categories ( 
                    id SERIAL PRIMARY KEY, 
                    name VARCHAR(20) NOT NULL 
                    );
            """,
            """ 
            CREATE TABLE IF NOT EXISTS records ( 
                    id SERIAL PRIMARY KEY,
                    user_id INT,
                    category_id INT, 
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    amount_of_expenditure FLOAT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                    );
            """)
        conn = None
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            for command in commands:
                cur.execute(command)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def add_data(self, data):
        self.db.session.add(data)
        self.db.session.commit()

    def upd_data(self):
        self.db.session.commit()

    def delete_data(self, data):
        self.db.session.delete(data)
        self.db.session.commit()
