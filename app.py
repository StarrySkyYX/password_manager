from flask import Flask,request,render_template,session
# from user import user
import sqlite3,os
from dotenv import load_dotenv
app = Flask(__name__)
conn = sqlite3.connect('data/password_manager.db')
c=conn.cursor()
# 讀取 .env 檔案
load_dotenv()
# 使用環境變數
app.secret_key = os.getenv('SECRET_KEY')
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
    if request.method=="POST":
        user_mail=request.form['user_mail']
        password=request.form['password']
        if check(user_mail,password):
            session[user_mail]=user.search(user_mail)
            return render_template("home.html", session[user_mail].name,session[user_mail].get())
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
            session[request.form['user_mail']]=user(name=request.form['user_name'])
            insert_Users(request.form['user_mail'],request.form['password'])
            add_table(request.form['user_mail'])
            return render_template("home.html", session[request.form['user_mail']].name)
    return render_template('register.html',error=error)
    
# 
# 因不知道Button和RadioButton在request.form所儲存的key-value，因此向chatGPT詢問 
@app.route('/home', methods=['POST'])
def home():
    if 'button_edit' in request.form:
        return render_template('edit.html',request.form['keyword'],request.form['account_id'],request.form['account_password'])
    elif 'button_add' in request.form:
        return render_template('add.html')
    elif 'button_delete' in request.form:
        user_info=session.get("user_mail")
        user_info.delete()
        return render_template("home.html", user_info.name,user_info.get())


@app.route('/edit', methods=['POST'])
def edit():
    user_info=session.get("user_mail")
    if request.method=="POST":
        user_info.edit(request.form['keyword'],request.form['account_id'],request.form['account_password'])
        return render_template("home.html", user_info.name,user_info.get())

@app.route('/add', methods=['POST'])
def add():
    user_info=session.get("user_mail")
    if request.method=="POST":
        user_info.add(request.form['keyword'],request.form['account_id'],request.form['account_password'])
        return render_template("home.html", user_info.name,user_info.get())




    

if __name__ == '__main__':
    app.run(debug=True)




