from flask import Flask,request,render_template
from user import User


app = Flask(__name__)
login_user={}
@app.route('/websites/home', methods=['POST', 'GET'])
def home():
    # user_agent= request.headers.get('User-Agent')
    print(request.form["keyword"])
    # if 'button_edit' in request.form:
        
    # elif 'button_add' in request.form:
    #     login_user[user_agent].add(request.form['keyword'],request.form['account_id'],request.form['account_password'])
    #     return render_template('/websites/home.html', user_info=User.load(login_user[user_agent].name))
    # elif 'button_delete' in request.form:
    #     login_user[user_agent].delete(request.form['keyword'])
    #     return render_template("/websites/home.html", user_info=User.load(login_user[user_agent].name))
    # elif 'button_logout' in request.form:
    #     del login_user[user_agent]
    #     return render_template("index.html")  
    # return render_template("/websites/home.html", user_info=User.load(login_user[user_agent].name))