#encoding: utf-8
from flask import Flask,render_template,Blueprint
from orgManagement import org_manage

app = Flask(__name__)

#注册蓝图
app.register_blueprint(org_manage)
 
@app.route("/")
def hello():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)