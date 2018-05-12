import sys
sys.path.append(sys.path[0] + '\\app')
reload(sys)
sys.setdefaultencoding("utf-8")


from app import create_app
from flask_script import Manager,Server


# manager = Manager(create_app())

# manager.add_command("runserver", Server())

if __name__ == "__main__":
    create_app('default').run(debug = True)
    # manager.run()