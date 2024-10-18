#!/usr/bin/env python3
"""
Flask app for monster creation in Pathfinder 1e.
To be used as a tool for Dungeon Master's looking to quickly make custom monsters.
"""
import traceback
import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from src.monster_balancer.monster_balancer import get_statistic_column, armor_class_deviated, determine_cr_float, generate_list_of_dictionaries, MONSTER_STATISTICS_BY_CR

app = Flask(__name__)
app.secret_key = re.sub(r"[^a-z\d]", "", os.path.realpath(__file__))

ORIGIN_INDEX = 1

@app.route("/")
def main():
    """ Main route """
    session["ac"] = get_statistic_column("Armor Class")[ORIGIN_INDEX]
    session["cr"] = ORIGIN_INDEX
    session["hp"] = get_statistic_column("Hit Points")[ORIGIN_INDEX]
    return render_template("index.html")

@app.route("/settings")
def settings():
    """ Settings route """
    return render_template("settings.html")

@app.route("/creature-designer")
def creature_designer():
    """ Creature designer route """
    return render_template("creature-designer.html")

@app.route("/monster-balancer")
def monster_balancer():
    """ Monster balancer route """
    session["average_ac_for_cr"] = get_statistic_column("Armor Class")[int(session["cr"])]
    session["ac_deviation"] = armor_class_deviated(session["ac"], session["cr"])
    session["cr_value_for_ac"] = determine_cr_float("Armor Class", int(session["ac"]))
    ac_column = get_statistic_column("Armor Class")
    min_ac = ac_column[0]
    max_ac = ac_column[-1]
    hp_column = get_statistic_column("Hit Points")
    min_hp = hp_column[0]
    max_hp = hp_column[-1]
    return render_template(
        "monster-balancer.html",
        current_ac = session["ac"],
        current_cr = session["cr"],
        current_hp = session["hp"],
        average_ac_for_cr = session["average_ac_for_cr"],
        ac_deviation = session["ac_deviation"],
        min_ac = min_ac,
        max_ac = max_ac,
        min_hp = min_hp,
        max_hp = max_hp,
        )

@app.route('/update-monster-balancer-ac', methods=['POST'])
def update_content_monster_balancer_ac():
    """ AC Update route for monster balancer"""
    session["ac"] = request.json['acSliderValue']
    session["ac_deviation"] = armor_class_deviated(session["ac"], session["cr"])
    session["cr_value_for_ac"] = determine_cr_float("Armor Class", int(session["ac"]))
    return jsonify(
        ac_deviation=session["ac_deviation"],
        cr_value_for_ac=session["cr_value_for_ac"],
                   )

@app.route('/update-monster-balancer-hp', methods=['POST'])
def update_content_monster_balancer_hp():
    """ HP Update route for monster balancer"""
    session["hp"] = request.json['hpSliderValue']

    return jsonify(
        expected_cr_for_hp = determine_cr_float("Hit Points", int(session["hp"]))
                   )

@app.route('/update-monster-balancer-cr', methods=['POST'])
def update_content_monster_balancer_cr():
    """ CR Update route for monster balancer"""
    session["cr"] = request.json['crSliderValue']

    average_ac_for_cr = get_statistic_column("Armor Class")[int(session["cr"])]
    ac_column = get_statistic_column("Armor Class")
    average_ac_for_cr = ac_column[int(session["cr"])]

    average_hp_for_cr = get_statistic_column("Hit Points")[int(session["cr"])]

    session["ac_deviation"] = armor_class_deviated(session["ac"], session["cr"])
    session["cr_value_for_ac"] = determine_cr_float("Armor Class", int(session["ac"]))

    return jsonify(
        average_ac_for_cr = average_ac_for_cr,
        ac_deviation = session["ac_deviation"],
        cr_value_for_ac = session["cr_value_for_ac"],
        average_hp_for_cr = average_hp_for_cr
        )

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
