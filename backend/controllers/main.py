
from flask import  Blueprint

bp = Blueprint('api', __name__, url_prefix="/api")

from controllers.items import *
from controllers.auth import *
from controllers.rental import *
from controllers.users import *