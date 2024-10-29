#!/usr/bin/env python3
"""
Flask app for monster creation in Pathfinder 1e.
To be used as a tool for Dungeon Master's looking to quickly make custom monsters.
"""
import traceback
import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from src.monster_balancer.monster_balancer import get_average_damage_column, get_statistic_column, armor_class_deviated, determine_cr_float, generate_list_of_dictionaries, MONSTER_STATISTICS_BY_CR

app = Flask(__name__)
app.secret_key = re.sub(r"[^a-z\d]", "", os.path.realpath(__file__))

ORIGIN_INDEX = 1

@app.route("/")
def main():
    """ Main route """
    return render_template("index.html")

@app.route('/reset-session')
def reset_session():
    """ Clear session. """
    session.clear()
    return redirect(url_for('main'))


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
    if not session.get("cr", None):
        session["cr"] = ORIGIN_INDEX
    if not session.get("ac"):
        session["ac"] = get_statistic_column("Armor Class")[int(session["cr"])]
    if not session.get("hp"):
        session["hp"] = get_statistic_column("Hit Points")[int(session["cr"])]
    if not session.get("damage"):
        session["damage"] = get_average_damage_column()[int(session["cr"])]

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
    saves = ["fortitude", "reflex", "will"]
    good_save_column = get_statistic_column("Good Save")
    poor_save_column = get_statistic_column("Poor Save")
    min_good_save, max_good_save = good_save_column[0], good_save_column[-1]
    min_poor_save, max_poor_save = poor_save_column[0], poor_save_column[-1]
    saves_checkbox = {
        "fortitude": session.get('fortitudeIsGoodSave', False),
        "reflex": session.get('reflexIsGoodSave', False),
        "will": session.get('willIsGoodSave', False),
    }

    min_saves = {
        "fortitude": min_good_save if saves_checkbox["fortitude"] else min_poor_save,
        "reflex": min_good_save if saves_checkbox["reflex"] else min_poor_save,
        "will": min_good_save if saves_checkbox["will"] else min_poor_save,
    }
    max_saves = {
        "fortitude": max_good_save if saves_checkbox["fortitude"] else max_poor_save,
        "reflex": max_good_save if saves_checkbox["reflex"] else max_poor_save,
        "will": max_good_save if saves_checkbox["will"] else max_poor_save,
    }

    session["current_fortitude"] = session.get('current_fortitude', good_save_column[int(session["cr"])])
    session["current_reflex"] = session.get('current_reflex', good_save_column[int(session["cr"])])
    session["current_will"] = session.get('current_will', good_save_column[int(session["cr"])])

    current_saves = {
        "fortitude": session["current_fortitude"],
        "reflex": session["current_reflex"],
        "will": session["current_will"],
    }

    average_good_save_for_cr = get_statistic_column("Good Save")[int(session["cr"])]
    average_poor_save_for_cr = get_statistic_column("Poor Save")[int(session["cr"])]

    average_saves_for_cr = {}
    for save in saves:
        if saves_checkbox[save]:
            average_saves_for_cr[save] = good_save_column[int(session["cr"])]
        else:
            average_saves_for_cr[save] = poor_save_column[int(session["cr"])]

    for save, is_good_save in saves_checkbox.items():
        if is_good_save:
            average_saves_for_cr[save] = get_statistic_column("Good Save")[int(session["cr"])]
        else:
            average_saves_for_cr[save] = get_statistic_column("Poor Save")[int(session["cr"])]

    expected_cr_for_save = {
        "fortitude": determine_cr_float("Good Save" if saves_checkbox["fortitude"] else "Poor Save", current_saves["fortitude"]),
        "reflex": determine_cr_float("Good Save" if saves_checkbox["reflex"] else "Poor Save", current_saves["reflex"]),
        "will": determine_cr_float("Good Save" if saves_checkbox["will"] else "Poor Save", current_saves["will"]),
    }

    # Attacks
    if not session.get("attack", None):
        session["attack"] = get_statistic_column("High Attack")[0]
    min_attack = get_statistic_column("Low Attack")[0]
    max_attack = get_statistic_column("Low Attack")[-1]

    if session.get('average_attack_for_cr', None):
        average_attack_for_cr = session['average_attack_for_cr']
    else:
        average_attack_for_cr = get_statistic_column("Low Attack")[int(session["cr"])]

    if session.get('expected_cr_for_attack', None):
        expected_cr_for_attack = session['expected_cr_for_attack']
    else:
        expected_cr_for_attack = determine_cr_float("Low Attack", int(session["attack"]))

    is_primarily_attacker = session.get('is_primarily_attacker', False)

    # Dice Checks
    if not session.get("dc", None):
        session["dc"] = get_statistic_column("Primary Ability DC")[0]
    if not session.get("ability_reliant", None):
        session["ability_reliant"] = False
    dc_column = get_statistic_column("Primary Ability DC" if session.get("ability_reliant") else "Secondary Ability DC")
    min_dc = dc_column[0]
    max_dc = dc_column[-1]

    if session.get('average_dc_for_cr', None):
        average_dc_for_cr = session['average_dc_for_cr']
    else:
        average_dc_for_cr = get_statistic_column("Secondary Ability DC")[int(session["cr"])]

    if session.get('expected_cr_for_dc', None):
        expected_cr_for_dc = session['expected_cr_for_dc']
    else:
        expected_cr_for_dc = determine_cr_float("Secondary Ability DC", int(session["dc"]))

    # Damage
    damage_column = get_average_damage_column()
    min_damage = damage_column[0]
    max_damage = damage_column[-1]
    if session.get('damage', None):
        current_damage = session['damage']
    else:
        current_damage = damage_column[0]
    expected_cr_for_damage = determine_cr_float("Damage", int(current_damage))
    session["average_damage_for_cr"] = determine_cr_float("Damage", int(session["damage"]))
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
        min_saves=min_saves,
        max_saves=max_saves,
        current_saves=current_saves,
        saves_checkbox=saves_checkbox,
        min_good_save=min_good_save,
        max_good_save=max_good_save,
        min_poor_save=min_poor_save,
        max_poor_save=max_poor_save,
        average_good_save_for_cr=average_good_save_for_cr,
        average_poor_save_for_cr=average_poor_save_for_cr,
        expected_cr_for_save=expected_cr_for_save,
        average_saves_for_cr=average_saves_for_cr,
        current_attack=session["attack"],
        min_attack=min_attack,
        max_attack=max_attack,
        average_attack_for_cr=average_attack_for_cr,
        expected_cr_for_attack=expected_cr_for_attack,
        is_primarily_attacker=is_primarily_attacker,
        min_dc=min_dc,
        max_dc=max_dc,
        average_dc_for_cr=average_dc_for_cr,
        expected_cr_for_dc=expected_cr_for_dc,
        current_dc=session["dc"],
        relies_on_abilities=session.get('relies_on_abilities', False),
        min_damage=min_damage,
        max_damage=max_damage,
        current_damage=current_damage,
        expected_cr_for_damage=expected_cr_for_damage,
        average_damage_for_cr=session["average_damage_for_cr"],
        )

@app.route('/update-monster-balancer-saves', methods=['POST'])
def update_content_monster_balancer_saves():
    """ Saves Update route for monster balancer"""
    save = request.json['save']
    session["current_" + save] = request.json['sliderValue']
    if request.json['isGoodSave']:
        expected_cr_for_save = determine_cr_float("Good Save", int(session["current_" + save]))
        session[save + 'isGoodSave'] = True
    else:
        expected_cr_for_save = determine_cr_float("Poor Save", int(session["current_" + save]))
        session[save + 'isGoodSave'] = False

    return jsonify(
        expected_cr_for_save=expected_cr_for_save,
                   )

@app.route('/update-monster-balancer-saves-checked-box', methods=['POST'])
def update_content_monster_balancer_saves_checked_box():
    """ Saves Update route for monster balancer"""
    slider_value = int(request.json['sliderValue'])
    save = request.json['save']

    if request.json['isGoodSave']:
        min_save = get_statistic_column("Good Save")[0]
        max_save = get_statistic_column("Good Save")[-1]
        slider_value = max(slider_value, min_save)
        expected_cr_for_save = determine_cr_float("Good Save", slider_value)
        average_save_for_cr = get_statistic_column("Good Save")[int(session["cr"])]
        session[save + 'IsGoodSave'] = True
    else:
        min_save = get_statistic_column("Poor Save")[0]
        max_save = get_statistic_column("Poor Save")[-1]
        slider_value = min(slider_value, max_save)
        expected_cr_for_save = determine_cr_float("Poor Save", slider_value)
        average_save_for_cr = get_statistic_column("Poor Save")[int(session["cr"])]
        session[save + 'IsGoodSave'] = False

    session["current_" + save] = slider_value
    return jsonify(
        min_save=min_save,
        max_save=max_save,
        expected_cr_for_save=expected_cr_for_save,
        average_save_for_cr=average_save_for_cr,
        slider_value=slider_value,
                   )

@app.route('/update-monster-balancer-attack', methods=['POST'])
def update_content_monster_balancer_attack():
    """ Attack Update route for monster balancer"""
    session["attack"] = request.json['sliderValue']
    if request.json['primarilyAttacker']:
        expected_cr_for_attack = determine_cr_float("High Attack", int(session["attack"]))
    else:
        expected_cr_for_attack = determine_cr_float("Low Attack", int(session["attack"]))
    session["expected_cr_for_attack"] = expected_cr_for_attack

    return jsonify(
        expected_cr_for_attack=expected_cr_for_attack,
                   )

@app.route('/update-monster-balancer-dc', methods=['POST'])
def update_content_monster_balancer_dc():
    """ DC Update route for monster balancer"""
    slider_value = int(request.json['sliderValue'])
    if request.json['abilityReliant']:
        expected_cr_for_dc = determine_cr_float("Primary Ability DC", slider_value)
    else:
        expected_cr_for_dc = determine_cr_float("Secondary Ability DC", slider_value)
    session["expected_cr_for_dc"] = expected_cr_for_dc

    dc_below_minimum = slider_value < get_statistic_column("Secondary Ability DC")[int(session["cr"])]


    session["dc"] = slider_value
    return jsonify(
        expected_cr_for_dc=expected_cr_for_dc,
        dc_below_minimum=dc_below_minimum,
                   )

@app.route('/update-monster-balancer-attack-checked-box', methods=['POST'])
def update_content_monster_balancer_attack_checked_box():
    """ Attacks Update checked box route for monster balancer"""
    slider_value = int(request.json['sliderValue'])

    if request.json['primarilyAttacker']:
        min_value = get_statistic_column("High Attack")[0]
        max_value = get_statistic_column("High Attack")[-1]
        slider_value = max(slider_value, min_value)
        expected_cr_for_value = determine_cr_float("High Attack", slider_value)
        average_value_for_cr = get_statistic_column("High Attack")[int(session["cr"])]
    else:
        min_value = get_statistic_column("Low Attack")[0]
        max_value = get_statistic_column("Low Attack")[-1]
        slider_value = min(slider_value, max_value)
        expected_cr_for_value = determine_cr_float("Low Attack", slider_value)
        average_value_for_cr = get_statistic_column("Low Attack")[int(session["cr"])]

    session["attack"] = slider_value
    session["is_primarily_attacker"] = request.json['primarilyAttacker']
    return jsonify(
        min_value=min_value,
        max_value=max_value,
        expected_cr_for_value=expected_cr_for_value,
        average_value_for_cr=average_value_for_cr,
        slider_value=slider_value,
                   )

@app.route('/update-monster-balancer-dc-checked-box', methods=['POST'])
def update_content_monster_balancer_dc_checked_box():
    """ DC Update checked box route for monster balancer"""
    slider_value = int(request.json['sliderValue'])

    if request.json['abilityReliant']:
        min_value = get_statistic_column("Primary Ability DC")[0]
        max_value = get_statistic_column("Primary Ability DC")[-1]
        slider_value = max(slider_value, min_value)
        expected_cr_for_value = determine_cr_float("Primary Ability DC", slider_value)
        average_value_for_cr = get_statistic_column("Primary Ability DC")[int(session["cr"])]
    else:
        min_value = get_statistic_column("Secondary Ability DC")[0]
        max_value = get_statistic_column("Secondary Ability DC")[-1]
        slider_value = min(slider_value, max_value)
        expected_cr_for_value = determine_cr_float("Secondary Ability DC", slider_value)
        average_value_for_cr = get_statistic_column("Secondary Ability DC")[int(session["cr"])]
    session["relies_on_abilities"] = request.json['abilityReliant']
    session["dc"] = slider_value
    return jsonify(
        min_value=min_value,
        max_value=max_value,
        expected_cr_for_value=expected_cr_for_value,
        average_value_for_cr=average_value_for_cr,
        slider_value=slider_value,
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
    if request.json['isGoodSaveFort']:
        average_save_for_cr_fortitude = get_statistic_column("Good Save")[int(session["cr"])]
    else:
        average_save_for_cr_fortitude = get_statistic_column("Poor Save")[int(session["cr"])]
    if request.json['isGoodSaveWill']:
        average_save_for_cr_will = get_statistic_column("Good Save")[int(session["cr"])]
    else:
        average_save_for_cr_will = get_statistic_column("Poor Save")[int(session["cr"])]

    if request.json['isPrimarilyAttacker']:
        average_attack_for_cr = get_statistic_column("High Attack")[int(session["cr"])]
    else:
        average_attack_for_cr = get_statistic_column("Low Attack")[int(session["cr"])]
    session['average_attack_for_cr'] = average_attack_for_cr

    if request.json['isAbilityReliant']:
        average_dc_for_cr = get_statistic_column("Primary Ability DC")[int(session["cr"])]
    else:
        average_dc_for_cr = get_statistic_column("Secondary Ability DC")[int(session["cr"])]
    session["average_dc_for_cr"] = average_dc_for_cr

    session["average_damage_for_cr"] = get_average_damage_column()[int(session["cr"])]
    return jsonify(
        average_ac_for_cr = average_ac_for_cr,
        ac_deviation = session["ac_deviation"],
        expected_hp_for_cr = average_hp_for_cr,
        average_save_for_cr_reflex=average_save_for_cr_reflex,
        average_save_for_cr_fortitude=average_save_for_cr_fortitude,
        average_save_for_cr_will=average_save_for_cr_will,
        average_attack_for_cr=average_attack_for_cr,
        average_dc_for_cr=average_dc_for_cr,
        average_damage_for_cr=session["average_damage_for_cr"],
        )

@app.route('/update-monster-balancer-damage', methods=['POST'])
def update_content_monster_balancer_damage():
    """ Damage Update route for monster balancer"""
    session["damage"] = request.json['damageSliderValue']

    return jsonify(
        expected_cr_for_damage = determine_cr_float("Damage", float(session["damage"]))
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
