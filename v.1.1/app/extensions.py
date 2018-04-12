from flask_uploads import UploadSet, IMAGES
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

__all__ = ['bootstrap', 'db', 'photos', 'login_manager']

bootstrap = Bootstrap()
db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)
login_manager = LoginManager()