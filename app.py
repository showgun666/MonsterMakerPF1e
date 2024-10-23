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

    # Armor Class
    ac_column = get_statistic_column("Armor Class")
    min_ac = ac_column[0]
    max_ac = ac_column[-1]

    # Hit Points
    hp_column = get_statistic_column("Hit Points")
    min_hp = hp_column[0]
    max_hp = hp_column[-1]

    # Saving throws
    saves = ["reflex", "fortitude", "will"]
    good_save_column = get_statistic_column("Good Save")
    poor_save_column = get_statistic_column("Poor Save")
    min_good_save = good_save_column[0]
    max_good_save = good_save_column[-1]
    min_poor_save = poor_save_column[0]
    max_poor_save = poor_save_column[-1]
    current_saves = {
        saves[0]:min_poor_save,
        saves[1]:min_poor_save,
        saves[2]:min_poor_save
    }

    average_good_save_for_cr = get_statistic_column("Good Save")[int(session["cr"])]
    average_poor_save_for_cr = get_statistic_column("Poor Save")[int(session["cr"])]
    expected_cr_for_good_save = determine_cr_float("Good Save", min_good_save)
    expected_cr_for_poor_save = determine_cr_float("Poor Save", min_poor_save)

    if not session.get("fort", None):
        session["fort"] = current_saves[saves[0]]
    if not session.get("ref", None):
        session["ref"] = current_saves[saves[1]]
    if not session.get("will", None):
        session["will"] = current_saves[saves[2]]

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
        expected_cr_for_hp = determine_cr_float("Hit Points", int(session["hp"])),
        expected_hp_for_cr = get_statistic_column("Hit Points")[int(session["cr"])],
        cr_value_for_ac=session["cr_value_for_ac"],
        saves=saves,
        min_good_save=min_good_save,
        max_good_save=max_good_save,
        min_poor_save=min_poor_save,
        max_poor_save=max_poor_save,
        current_saves=current_saves,
        average_good_save_for_cr=average_good_save_for_cr,
        average_poor_save_for_cr=average_poor_save_for_cr,
        expected_cr_for_good_save=expected_cr_for_good_save,
        expected_cr_for_poor_save=expected_cr_for_poor_save,
        )

@app.route('/update-monster-balancer-saves-ref', methods=['POST'])
def update_content_monster_balancer_saves_ref():
    """ Saves Update route for monster balancer"""
    session["ref"] = request.json['refSliderValue']
    if request.json['isGoodSave']:
        expected_cr_for_reflex = determine_cr_float("Good Save", int(session["ref"]))
    else:
        expected_cr_for_reflex = determine_cr_float("Poor Save", int(session["ref"]))

    return jsonify(
        expected_cr_for_reflex=expected_cr_for_reflex,
                   )
@app.route('/update-monster-balancer-saves-checked-box-ref', methods=['POST'])
def update_content_monster_balancer_saves_checked_box_ref():
    """ Saves Update route for monster balancer"""
    ref_slider_value = int(request.json['refSliderValue'])

    if request.json['isGoodSave']:
        min_save = get_statistic_column("Good Save")[0]
        max_save = get_statistic_column("Good Save")[-1]
        ref_slider_value = max(ref_slider_value, min_save)
        expected_cr_for_reflex = determine_cr_float("Good Save", ref_slider_value)
        average_save_for_cr_reflex = get_statistic_column("Good Save")[int(session["cr"])]
    else:
        min_save = get_statistic_column("Poor Save")[0]
        max_save = get_statistic_column("Poor Save")[-1]
        ref_slider_value = min(ref_slider_value, max_save)
        expected_cr_for_reflex = determine_cr_float("Poor Save", ref_slider_value)
        average_save_for_cr_reflex = get_statistic_column("Poor Save")[int(session["cr"])]

    session["ref"] = ref_slider_value
    return jsonify(
        min_save=min_save,
        max_save=max_save,
        expected_cr_for_reflex=expected_cr_for_reflex,
        average_save_for_cr_reflex=average_save_for_cr_reflex,
        ref_slider_value=ref_slider_value,
                   )

@app.route('/update-monster-balancer-saves-fort', methods=['POST'])
def update_content_monster_balancer_saves_fort():
    """ Saves Update route for monster balancer"""
    session["fort"] = request.json['fortSliderValue']

    return jsonify(
        expected_cr_for_fort_good=determine_cr_float("Good Save", int(session["fort"])),
        expected_cr_for_fort_poor=determine_cr_float("Poor Save", int(session["fort"])),
                   )
@app.route('/update-monster-balancer-saves-will', methods=['POST'])
def update_content_monster_balancer_saves_will():
    """ Saves Update route for monster balancer"""
    session["will"] = request.json['willSliderValue']

    return jsonify(
        expected_cr_for_will_good=determine_cr_float("Good Save", int(session["will"])),
        expected_cr_for_will_poor=determine_cr_float("Poor Save", int(session["will"])),
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

    if request.json['isGoodSaveRef']:
        average_save_for_cr_reflex = get_statistic_column("Good Save")[int(session["cr"])]
    else:
        average_save_for_cr_reflex = get_statistic_column("Poor Save")[int(session["cr"])]
    
    return jsonify(
        average_ac_for_cr = average_ac_for_cr,
        ac_deviation = session["ac_deviation"],
        expected_hp_for_cr = average_hp_for_cr,
        average_save_for_cr_reflex=average_save_for_cr_reflex,
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
