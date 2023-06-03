from flask import Flask
from flask import request
from flask import render_template
# from user import user
import sqlite3
app = Flask(__name__)
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
    error=""
    user_mail=request.form['user_mail']
    password=request.form['password']
    if request.method=="POST":
        if check(user_mail,password):
            login_user[user_mail]=user.search(user_mail)
            return render_template("home.html", login_user[user_mail].name)
        else:
            error="無效的使用者名稱/密碼"
    return render_template('login.html',error=error)
# 
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
    def insert_Users(user_mail,password):
        insert_user='''INSERT INTO Users VALUES (?,?)'''
        c.execute(insert_user,(user_mail,password,))
        conn.commit()

    # 一開始if語句嵌套過多層，可讀性差，詢問chatGPT解決辦法，他提議以elif來改善
    error=""
    if request.method=="POST":
        user_mail = request.form['user_mail']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user_name = request.form['user_name']
        if user_mail=="":
            error="電子郵件不得空白"
        elif not check(request.form['user_mail']):
            error="電子郵件已註冊"
        elif password=="":
            error="密碼不得空白"
        elif password!=confirm_password:
            error="密碼不一致"
        elif user_name=="":
            error="使用者名稱不得空白"
        else:
            login_user[request.form['user_mail']]=user(name=request.form['user_name'])
            insert_Users(request.form['user_mail'],request.form['password'])
            add_table(request.form['user_mail'])
            return render_template("home.html", login_user[request.form['user_mail']].name)
    return render_template('register.html',error=error)
    
# 
@app.route('/edit', methods=['POST', 'GET'])
def edit():
    
    

if __name__ == '__main__':
    app.run(debug=True)




