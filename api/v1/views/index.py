#!/usr/bin/python3
"""Return a JSON status:ok"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})
