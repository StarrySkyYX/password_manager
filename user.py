import sqlite3


class User:
    def __init__(self,user_mail):
        with sqlite3.connect('data/password_manager.db', check_same_thread=False) as conn:
            cursor=conn.cursor()
            self.mail=user_mail
            query='''SELECT name FROM Users WHERE mail=?'''
            self.name=''.join(cursor.execute(query, (self.mail,)).fetchall()[0])
            
        
    
    def delete(self,delete_keyword):
        with sqlite3.connect('data/password_manager.db', check_same_thread=False) as conn:
            cursor=conn.cursor()
            delete_sql_row='''DELETE FROM {} WHERE name=?;'''.format(self.name)
            cursor.execute(delete_sql_row,(delete_keyword,))
        
        
    def add(self,account_name,account_id,account_password):
        with sqlite3.connect('data/password_manager.db', check_same_thread=False) as conn:
            cursor=conn.cursor()
            insert_user='''INSERT INTO {} VALUES (?,?,?)'''.format(self.name)
            cursor.execute(insert_user,(account_name,account_id,account_password,))
    

    def edit(self,account_name,account_id,account_password):
        with sqlite3.connect('data/password_manager.db', check_same_thread=False) as conn:
            cursor=conn.cursor()
            edit_sql_str='''UPDATE {} SET id = ?, password = ? WHERE name = ?;'''.format(self.name)
            cursor.execute(edit_sql_str,(account_id,account_password,account_name,))
       

    

    @staticmethod
    def check_login(user_mail,password):
        with sqlite3.connect('data/password_manager.db', check_same_thread=False) as conn:
            cursor=conn.cursor()
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
        with sqlite3.connect('data/password_manager.db', check_same_thread=False) as conn:
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
        with sqlite3.connect('data/password_manager.db', check_same_thread=False) as conn:
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
        with sqlite3.connect('data/password_manager.db', check_same_thread=False) as conn:
            cursor=conn.cursor()
            insert_user='''INSERT INTO Users VALUES (?,?,?)'''
            cursor.execute(insert_user,(user_mail,password,user_name,))

    @staticmethod
    def add_table(user_name):
        with sqlite3.connect('data/password_manager.db' ,check_same_thread=False) as conn:
            cursor=conn.cursor()
            add_sql_table='''
            CREATE TABLE {} (
                "name"  TEXT NOT NULL,
                "id"     TEXT NOT NULL,
                "password"   TEXT NOT NULL,
                PRIMARY KEY("name")
                )
            '''.format(user_name)
            cursor.execute(add_sql_table)

    @staticmethod   
    def load(name):
        with sqlite3.connect('data/password_manager.db', check_same_thread=False) as conn:
            cursor=conn.cursor()
            query = '''SELECT * FROM {}'''.format(name)
            cursor.execute(query)
            rows = cursor.fetchall()
            result=[]
            for row_tuple in rows:
                result.append({
                    "name":row_tuple[0],
                    "id":row_tuple[1],
                "password":row_tuple[2]
                                    })
            return result
