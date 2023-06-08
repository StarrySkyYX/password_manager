import sqlite3

class User:
    def __init__(self,user_mail):
        """Initialize the User object.
        :param user_mail: User's mail
        """
        # Get the user name when initializing the User object
        with sqlite3.connect('data/password_manager.db', check_same_thread=False) as conn:
            cursor=conn.cursor()
            self.mail=user_mail
            query='''SELECT name FROM Users WHERE mail=?'''
            self.name=''.join(cursor.execute(query, (self.mail,)).fetchall()[0])
            conn.commit()
            
    def delete(self,delete_keyword):
        """Delete the ID and password stored by the user.
        :param delete_keyword: The name of the ID and password to be deleted by the User.
        """
        with sqlite3.connect('data/password_manager.db', check_same_thread=False) as conn:
            cursor=conn.cursor()
            delete_sql_row='''DELETE FROM {} WHERE name=?'''.format(self.name)
            cursor.execute(delete_sql_row,(delete_keyword,))
            conn.commit()
        
    def add(self,account_name,account_id,account_password):
        """Add the ID and password stored by the user.
        :param account_name: The name of the account to be added by the User.
        :param account_id: The ID of the account to be added by the User.
        :param account_name: The password of the account to be added by the User.
        """
        with sqlite3.connect('data/password_manager.db', check_same_thread=False) as conn:
            cursor=conn.cursor()
            insert_user='''INSERT INTO {} VALUES (?,?,?)'''.format(self.name)
            cursor.execute(insert_user,(account_name,account_id,account_password,))
            conn.commit()
    
    def edit(self,account_name,account_id,account_password):
        """Edit the ID and password stored by the user.
        :param account_name: The name of the account to be added by the User.
        :param account_id: The ID of the account to be added by the User.
        :param account_name: The password of the account to be added by the User.
        """
        with sqlite3.connect('data/password_manager.db', check_same_thread=False) as conn:
            cursor=conn.cursor()
            edit_sql_str='''UPDATE {} SET id = ?, password = ? WHERE name = ?;'''.format(self.name)
            cursor.execute(edit_sql_str,(account_id,account_password,account_name,))
            conn.commit()
       
    @staticmethod
    def check_login(user_mail,password):
        """Check user login
        :param user_mail: Email inputed by user
        :param password: password inputed by user
        """
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
        """Check if User exists
        :param user_mail: Email inputed by user
        """
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
        """Check if the name be used.
        :param user_mail: Email inputed by user
        """
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
        """Insert new User into SQL
        :param user_mail: Email of the new User.
        :param password: Password of the new User.
        :param user_name: Name of the new User.
        """
        with sqlite3.connect('data/password_manager.db', check_same_thread=False) as conn:
            cursor=conn.cursor()
            insert_user='''INSERT INTO Users VALUES (?,?,?)'''
            cursor.execute(insert_user,(user_mail,password,user_name,))
            conn.commit()

    @staticmethod
    def add_table(user_name):
        """Create new table into SQL for the new user
        :param user_name: Name of the new user.
        """
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
            conn.commit()

    @staticmethod   
    def load(user_name)->list:
        """Load user stored information.
        :param user_name: Name of the user.
        """
        with sqlite3.connect('data/password_manager.db', check_same_thread=False) as conn:
            cursor=conn.cursor()
            query = '''SELECT * FROM {}'''.format(user_name)
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
