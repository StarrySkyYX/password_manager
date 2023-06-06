import sqlite3
import atexit
conn = sqlite3.connect('data/password_manager.db')
cursor=conn.cursor()
# gpt
def close_db_conn():
    conn.close()
atexit.register(close_db_conn)

class User:
    name=""
    mail=""
    def __init__(self,user_mail):
        conn = sqlite3.connect('data/password_manager.db')
        cursor=conn.cursor()
        self.mail=user_mail
        query='''SELECT name FROM Users WHERE mail LIKE ?'''
        result=cursor.execute(query, (user_mail,)).fetchall()
        self.name=result[0]

    def __init__(self,user_mail,user_name):
        conn = sqlite3.connect('data/password_manager.db')
        cursor=conn.cursor()
        self.mail=user_mail
        self.name=user_name


    def search(self,search_str):
        rows=self.load
        for row in rows:
            if row['name']==search_str:
                return row

    def load(self):
        conn = sqlite3.connect('data/password_manager.db')
        cursor=conn.cursor()
        query='''SELECT * FROM table_name'''.replace('table_name',self.name)
        cursor.execute(query,(self.mail,))
        rows=cursor.fetchall()
        # 詢問如何把搜尋結果轉成字典
        return [dict(row) for row in rows] 
    
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
        # 執行查詢，將具體值綁定到佔位符
        cursor.execute(query, (user_mail,))
        # 獲取查詢結果
        check_password =(cursor.fetchall())[0]
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
