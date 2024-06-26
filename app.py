from flask import Flask
from flask import request
from flask import render_template
import sys
from flask import jsonify
from user import User

app = Flask(__name__)
login_user={}

@app.route('/', methods=['POST', 'GET'])
def load_index():
    '''Return index.html template
    '''
    return render_template('index.html')

@app.route('/websites/login', methods=['POST', 'GET'])
def login():
    '''Handle the login function.'''
    error=""
    if request.method=="POST":
        user_mail=request.form['user_mail']
        password=request.form['password']
        if User.check_login(user_mail,password):
            user_agent= request.headers.get('User-Agent')
            login_user[user_agent]=User(user_mail)
            return render_template('/websites/home.html',
                                    user_info=User.load(login_user[user_agent].name))
        else:
            error="無效的使用者名稱/密碼"
    return render_template('/websites/login.html',error=error)

@app.route('/websites/register', methods=['POST', 'GET'])
def register():
    '''Handle the registration function.'''
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
            user_agent= request.headers.get('User-Agent')
            login_user[user_agent]=User(user_mail)
            return render_template('/websites/home.html',
                                    user_info=User.load(login_user[user_agent].name))
    return render_template('/websites/register.html', error=error)


@app.route('/websites/home', methods=['POST'])
def home():
    '''Load user's home page.'''
    user_agent= request.headers.get('User-Agent')
    if request.method=="POST":
        if 'button_logout' in request.form:
            del login_user[user_agent]
            sys.exit()
        else:
            return render_template("/websites/home.html", user_info=User.load(login_user[user_agent].name))

@app.route('/websites/delete', methods=['POST'])   
def delete():
    '''Handle user requests to delete data.'''
    if request.method=="POST":
        user_agent=request.headers.get('User-Agent')
        login_user[user_agent].delete(request.json.get('account_name'))

    return render_template("/websites/home.html", user_info=User.load(login_user[user_agent].name))
    
@app.route('/websites/add', methods=['POST'])   
def add():
    '''Handle user requests to add data.'''
    if request.method=="POST":
        user_agent=request.headers.get('User-Agent')
        login_user[user_agent].add(request.json.get('account_name'),request.json.get('account_id'),request.json.get('account_password'))
    return render_template('/websites/home.html', user_info=User.load(login_user[user_agent].name))
    
@app.route('/websites/edit', methods=['POST'])   
def edit():
    '''Handle user requests to edit data.'''
    if request.method=="POST":
        user_agent=request.headers.get('User-Agent')
        login_user[user_agent].edit(request.json.get('account_name'),request.json.get('account_id'),request.json.get('account_password'))
    return render_template('/websites/home.html', user_info=User.load(login_user[user_agent].name))

@app.route('/websites/generate_random_password', methods=['POST'])
def generate_random_password():
    if request.method=="POST":
        random_password=User.random_password()
        password_value = random_password[0]["random_password"]
        print(password_value)
        return jsonify(random_password=password_value)

if __name__ == '__main__':
    app.run(debug=True)
