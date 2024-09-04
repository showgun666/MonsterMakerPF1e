#!/usr/bin/env python3
"""
Flask app for monster creation in Pathfinder 1e.
To be used as a tool for Dungeon Master's looking to quickly make custom monsters.
"""
import traceback
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    """ Main route """
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    """
    Handler for page not found 404
    """
    #pylint: disable=unused-argument
    return "Flask 404 here, but not the page you requested."


@app.errorhandler(500)
def internal_server_error(e):
    """
    Handler for internal server error 500
    """
    #pylint: disable=unused-argument
    return "<p>Flask 500<pre>" + traceback.format_exc()

if __name__ == "__main__":
    app.run(debug=True)
