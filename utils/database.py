import psycopg2 as psql
from main import config


class DATABASE:
    def __init__(self):
        self.conn = psql.connect(
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST
        )

        self.cursor = self.conn.cursor()

    def create_tables(self):
        users_table = """create table if not exists users_table(
        id SERIAL,
        chat_id bigint primary key,
        full_name varchar(55) not null,
        username varchar(32) unique       
        )"""

        followers_table = """create table if not exists followers_table(
        person_chat_id bigint primary key references users_table(chat_id),
        follower_chat_id bigint references users_table(chat_id)       
        )"""

        self.cursor.execute(users_table)
        self.cursor.execute(followers_table)

        self.conn.commit()


    def get_user_by_chat_id(self, chat_id):
        query_get = f"select * from users_table where chat_id = '{chat_id}'"
        self.cursor.execute(query_get)
        response = self.cursor.fetchall()
        return response


    def get_user_by_username(self, username):
        query_get = f"select * from users_table where username = '{username}'"
        self.cursor.execute(query_get)
        response = self.cursor.fetchall()
        return response


    def add_user(self, data:dict):
        chat_id = data['chat_id']
        full_name = data['full_name']
        username = data['username']

        query = f"insert into users_table(chat_id, username,full_name) values('{chat_id}', '{username}','{full_name}')"
        self.cursor.execute(query)
        self.conn.commit()

    def update_username(self, data: dict):
        chat_id = data['chat_id']
        username = data['username']
        query = f"update users_table set username = '{username}' where chat_id = '{chat_id}'"
        self.cursor.execute(query)
        self.conn.commit()


    def update_name(self, data: dict):
        chat_id = data['chat_id']
        full_name = data['full_name']
        query = f"update users_table set full_name = '{full_name}' where chat_id = '{chat_id}'"
        self.cursor.execute(query)
        self.conn.commit()