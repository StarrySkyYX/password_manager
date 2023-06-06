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
        self.mail=user_mail
        query='''SELECT name FROM Users WHERE mail LIKE ?'''
        result=cursor.execute(query, (user_mail,)).fetchall()
        self.name=result[0]

    def search(self,search_str):
        rows=self.load
        for row in rows:
            if row['name']==search_str:
                return row

    def load(self):
        query='''SELECT * FROM {self.name}'''
        cursor.execute(query,(self.mail,))
        rows=cursor.fetchall()
        # 詢問如何把搜尋結果轉成字典
        return [dict(row) for row in rows] 
    
    def delete(self,delete_keyword):
        delete_sql_row='''DELETE FROM {self.name} WHERE name=?'''
        cursor.execute(delete_sql_row,(delete_keyword,))
        conn.commit()
        
    def add(self,keyword,account_id,account_password):
        insert_user='''INSERT INTO {self.name} VALUES (?,?,?)'''
        cursor.execute(insert_user,(keyword,account_id,account_password,))
        conn.commit()

    def edit(self,keyword,account_id,account_password):
        edit_sql_str='''UPDATE {self.name} SET id = ? password = ? WHERE name = ?'''
        cursor.execute(edit_sql_str,(account_id,account_password,keyword,))
        conn.commit()

    @staticmethod
    def check_login(user_mail,password):
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
        insert_user='''INSERT INTO Users VALUES (?,?,?)'''
        cursor.execute(insert_user,(user_mail,password,user_name,))
        conn.commit()
    @staticmethod
    def add_table(user_name):
        add_sql_table='''
        CREATE TABLE {name} (
            "name"  TEXT,
            "id"    TEXT,
            "password"  TEXT,
            PRIMARY KEY("name")
            )
        '''
        cursor.execute(add_sql_table)
        conn.commit()
