from flask import request
from flask import render_template
# from user import user
import sqlite3
conn = sqlite3.connect('data/password_manager.db')
c=conn.cursor()
login_user={}
# closs
@app.route('/login', methods=['POST', 'GET'])
def login():
    # 
    def check(user_mail,password):
        # 定義查詢語句和佔位符
        query = '''SELECT password FROM Users WHERE mail LIKE ?'''
        # 執行查詢，將具體值綁定到佔位符
        c.execute(query, (user_mail,))
        # 獲取查詢結果
        check_password =(c.fetchall())[0]
        if check_password==password:
            return True
        return False
    # 
    if request.method=="POST":
        if check(request.form['user_mail'],request.form['password']):
            login_user[request.form['user_mail']]=user.search(request.form['user_mail'])
            return render_template("home.html", login_user[request.form['user_mail']].name)
        else:
            error="無效的使用者名稱/密碼"
    return render_template('login.html',error=error)

@app.route('/register', methods=['POST', 'GET'])
def register():
    # 
    def check(user_mail):
        # 定義查詢語句和佔位符
        query = '''SELECT mail FROM Users WHERE mail LIKE ?'''
        # 執行查詢，將具體值綁定到佔位符
        c.execute(query, (user_mail,))
        if len(c.fetchall())==0:
            return True
        return False
    # 
    def add_table(user_mail):
        add_sql_table='''
        CREATE TABLE ? (
            "name"  TEXT,
            "id"    TEXT,
            "password"  TEXT,
            PRIMARY KEY("name")
            )
        '''
        c.execute(add_sql_table, (user_mail,))
        conn.commit()
    # 
    # def insert_sql_Users(user_mail,password):
    #     return

    # 
    if request.method=="POST":
        if check(request.form['user_mail']):
            if request.form['password']==request.form['confirm_password']:
                if request.form['user_name']!="":
                    login_user[request.form['user_mail']]=user(name=request.form['user_name'])
                    insert_sql_Users(request.form['user_mail'],request.form['password'])
                    add_table(request.form['user_mail'])
                    return render_template("home.html", login_user[request.form['user_mail']].name)
                else:
                    error="使用者名稱不得空白"
            else:
                error="密碼不一致"
        else:
            error="使用者已註冊"
    return render_template('register.html',error=error)





