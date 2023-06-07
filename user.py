import sqlite3
import atexit
import json
conn = sqlite3.connect('data/password_manager.db')
cursor=conn.cursor()
# gpt
def close_db_conn():
    conn.close()
atexit.register(close_db_conn)

class User:
    name=""
    mail=""
    account=[]
    def __init__(self,user_mail):
        conn = sqlite3.connect('data/password_manager.db')
        cursor=conn.cursor()
        self.mail=user_mail
        query='''SELECT name FROM Users WHERE mail=?'''
        self.name=''.join(cursor.execute(query, (self.mail,)).fetchall()[0])

    def __dict__(self):
        return {
            'name': self.name,
            'mail': self.mail,
            'account': self.account
        }

    def to_json(self):
        return json.dumps(self.__dict__())

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        user = User(data['mail'])
        user.name = data['name']
        user.account = data['account']
        return user

    
    def search(self,search_str):
        rows=self.load()
        for row in rows:
            if row['name']==search_str:
                return row
    
   
    def load(self):
        conn = sqlite3.connect('data/password_manager.db')
        cursor = conn.cursor()
        query = '''SELECT * FROM {}'''.format(self.name)
        cursor.execute(query)
        rows = cursor.fetchall()
        result=[]
        for row_tuple in rows:
            result.append({
                'name':row_tuple[0],
                'id':row_tuple[1],
                'password':row_tuple[2]
                                })
        self.account=result
        return result
        
    
    def delete(self,delete_keyword):
        conn = sqlite3.connect('data/password_manager.db')
        cursor=conn.cursor()
        delete_sql_row='''DELETE FROM table_name WHERE name=?'''.replace('table_name',self.name)
        cursor.execute(delete_sql_row,(delete_keyword,))
        conn.commit()

        
    def add(self,keyword,account_id,account_password):
        conn = sqlite3.connect('data/password_manager.db')
        cursor=conn.cursor()
        insert_user='''INSERT INTO table_name VALUES (?,?,?)'''.replace('table_name',self.name)
        cursor.execute(insert_user,(keyword,account_id,account_password,))
        conn.commit()


    def edit(self,keyword,account_id,account_password):
        conn = sqlite3.connect('data/password_manager.db')
        cursor=conn.cursor()
        edit_sql_str='''UPDATE table_name SET id = ? password = ? WHERE name = ?'''.replace('table_name',self.name)
        cursor.execute(edit_sql_str,(account_id,account_password,keyword,))
        conn.commit()

    


    @staticmethod
    def check_login(user_mail,password):
        conn = sqlite3.connect('data/password_manager.db')
        cursor=conn.cursor()
        # 定義查詢語句和佔位符
        query = '''SELECT password FROM Users WHERE mail LIKE ?'''
        result=cursor.execute(query, (user_mail,)).fetchall()
        if len(result)==0:
            return False
        check_password =''.join(result[0])
        if check_password==password:
            return True
        return False
    
    @staticmethod
    def check_mail_exist(user_mail):
        conn = sqlite3.connect('data/password_manager.db')
        cursor=conn.cursor()
        # 定義查詢語句和佔位符
        query = '''SELECT mail FROM Users WHERE mail LIKE ?'''
        # 執行查詢，將具體值綁定到佔位符
        cursor.execute(query, (user_mail,))
        if len(cursor.fetchall())==0:
            return True
        return False
    
    @staticmethod
    def check_name_exist(user_name):
        conn = sqlite3.connect('data/password_manager.db')
        cursor=conn.cursor()
        # 定義查詢語句和佔位符
        query = '''SELECT name FROM Users WHERE name LIKE ?'''
        # 執行查詢，將具體值綁定到佔位符
        cursor.execute(query, (user_name,))
        if len(cursor.fetchall())==0:
            return True
        return False
    
    @staticmethod
    def insert_user(user_mail,password,user_name):
        conn = sqlite3.connect('data/password_manager.db')
        cursor=conn.cursor()
        insert_user='''INSERT INTO Users VALUES (?,?,?)'''
        cursor.execute(insert_user,(user_mail,password,user_name,))
        conn.commit()
    @staticmethod
    def add_table(user_name):
        conn = sqlite3.connect('data/password_manager.db')
        cursor=conn.cursor()
        add_sql_table='''
        CREATE TABLE table_name (
            "name"  TEXT,
            "id"    TEXT,
            "password"  TEXT,
            PRIMARY KEY("name")
            )
        '''.replace('table_name',user_name)
        cursor.execute(add_sql_table)
        conn.commit()

