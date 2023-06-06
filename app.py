from flask import Flask,request,render_template,session
from user import User
import os
from dotenv import load_dotenv
import atexit,json

app = Flask(__name__)
# 讀取 .env 檔案
load_dotenv()
# 使用環境變數
app.secret_key = os.getenv('SECRET_KEY')
# closs
@app.route('/', methods=['POST', 'GET'])
def load_index():
    return render_template('index.html')

@app.route('/websites/login', methods=['POST', 'GET'])
def login():
    error=""
    if request.method=="POST":
        user_mail=request.form['user_mail']
        password=request.form['password']
        if User.check_login(user_mail,password):
            session[user_mail]=User(user_mail)
            user_name=session[user_mail].name
            user_info=json.dumps(session[user_mail].load())
            return render_template("/websites/home.html",user_name=user_name,user_info=user_info)
        else:
            error="無效的使用者名稱/密碼"
    return render_template('/websites/login.html',error=error)
# 
@app.route('/websites/register', methods=['POST', 'GET'])
def register():
    # 一開始if語句嵌套過多層，可讀性差，詢問chatGPT解決辦法，他提議以elif來改善
    error=""
    if request.method=="POST":
        user_mail = request.form['user_mail']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user_name = request.form['user_name']
        if user_mail=="":
            error="電子郵件不得空白"
        elif not User.check_mail_exist(request.form['user_mail']):
            error="電子郵件已註冊"
        elif not User.check_name_exist(request.form['user_name']):
            error="使用者名稱已被使用"
        elif password=="":
            error="密碼不得空白"
        elif password!=confirm_password:
            error="密碼不一致"
        elif user_name=="":
            error="使用者名稱不得空白"
        else:
            User.add_table(user_name)
            User.insert_user(user_mail,password,user_name)
            session[user_mail]=User(user_mail)
            user_info=json.dumps(session[user_mail].load())
            return render_template("/websites/home.html", user_name=session[user_mail].name,user_info=user_info)
    return render_template('/websites/register.html',error=error)
    
# 
# 因不知道Button和RadioButton在request.form所儲存的key-value，因此向chatGPT詢問 
@app.route('/websites/home', methods=['POST', 'GET'])
def home():
    if 'button_edit' in request.form:
        return render_template('/websites/edit.html',request.form['keyword'],request.form['account_id'],request.form['account_password'])
    elif 'button_add' in request.form:
        return render_template('/websites/add.html')
    elif 'button_delete' in request.form:
        user_object=session.get("user_mail")
        user_object.delete(request.form['keyword'])
        return render_template("/websites/home.html", user_name=user_object.name,user_info=user_object.load())
    elif 'search' in request.form:
        user_object=session.get("user_mail")
        return render_template("/websites/home.html", user_name=user_object.name,user_info=user_object.search(request.form['search'],))
    elif 'button_logout' in request.form:
        session.clear()
        return render_template("index.html")
    
@app.route('/websites/home', methods=['POST', 'GET'])
def edit():
    user=session.get("user_mail")
    if request.method=="POST":
        user.edit(request.form['keyword'],request.form['account_id'],request.form['account_password'],)
        return render_template("/websites/home.html", user_name=user.name,user_info=user.load())

@app.route('/websites/add', methods=['POST', 'GET'])
def add():
    user=session.get("user_mail")
    if request.method=="POST":
        user.add(request.form['keyword'],request.form['account_id'],request.form['account_password'],)
        return render_template("/websites/home.html", user_name=user.name,user_info=user.load())
    



if __name__ == '__main__':
    app.run(debug=True)

def clear_session():
    session.clear()

atexit.register(clear_session)



   


