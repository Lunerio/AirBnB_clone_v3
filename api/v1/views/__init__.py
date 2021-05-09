#!/usr/bin/python3
from flask import Blueprint


app_views = Blueprint("/api/v1", __name__)


from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.sities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
