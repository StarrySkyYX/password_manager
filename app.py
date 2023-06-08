from flask import Flask,request,render_template
from user import User
from flask_mail import Mail, Message


app = Flask(__name__)
login_user={}

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
            # gpt
            user_agent= request.headers.get('User-Agent')
            login_user[user_agent]=User(user_mail)
            return render_template('/websites/home.html', user_info=User.load(login_user[user_agent].name))
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
            user_agent= request.headers.get('User-Agent')
            login_user[user_agent]=User(user_mail)
            return render_template('/websites/home.html', user_info=User.load(login_user[user_agent].name))
    return render_template('/websites/register.html', error=error)
 # 因不知道Button和RadioButton在request.form所儲存的key-value，因此向chatGPT詢問 
@app.route('/websites/home', methods=['POST', 'GET'])
def home():
    user_agent= request.headers.get('User-Agent')
    if request.method=="POST":
        if 'button_logout' in request.form:
            del login_user[user_agent]
            return render_template("index.html")  
        return render_template("/websites/home.html", user_info=User.load(login_user[user_agent].name))
    

@app.route('/websites/delete', methods=['POST', 'GET'])   
def delete():
    if request.method=="POST":
        user_agent=request.headers.get('User-Agent')
        login_user[user_agent].delete(request.json.get('account_name'))
    return render_template("/websites/home.html", user_info=User.load(login_user[user_agent].name))
    
@app.route('/websites/add', methods=['POST', 'GET'])   
def add():
    if request.method=="POST":
        user_agent=request.headers.get('User-Agent')
        login_user[user_agent].add(request.json.get('account_name'),request.json.get('account_id'),request.json.get('account_password'))
    return render_template('/websites/home.html', user_info=User.load(login_user[user_agent].name))
    
@app.route('/websites/edit', methods=['POST', 'GET'])   
def edit():
    if request.method=="POST":
        user_agent=request.headers.get('User-Agent')
        login_user[user_agent].edit(request.json.get('account_name'),request.json.get('account_id'),request.json.get('account_password'))
    return render_template('/websites/home.html', user_info=User.load(login_user[user_agent].name))
    
# 設定郵件相關參數
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'peggyellachen585@gmail.com'  # 使用者的 Gmail 信箱
app.config['MAIL_PASSWORD'] = 'rehhigyqymkwnbwq'  # 使用者的 Gmail 密碼

mail = Mail(app)

# 定义联系页面的路由和处理函数
@app.route('/', methods=['POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        subject = request.form['subject']
        content = request.form['content']

        content = f"from:{email}\n\n{content}"

        # 创建邮件消息
        msg = Message(subject=subject, sender=email, recipients=['peggyellachen585@gmail.com'])
        msg.body = content

        # 发送邮件
        with app.app_context():
            mail.send(msg)
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)