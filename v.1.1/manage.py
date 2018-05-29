import sys
sys.path.append(sys.path[0] + '\\app')
reload(sys)
sys.setdefaultencoding("utf-8")


from app import create_app
from flask_script import Manager,Server

app = create_app('default')
app.host = '0.0.0.0'
manager = Manager(app)

manager.add_command("runserver", Server())
# manager.add_command('host','0.0.0.0')
# manager.add_command('debug', True)

if __name__ == "__main__":
    # create_app('default').run(debug = True)
    manager.run()