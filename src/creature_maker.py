#!/usr/bin/env python3
"""
Class for handling front end interactions with the creature
maker application.

"""
from src.constants import DAMAGE_DICE_PROGRESSION, MONSTER_STATISTICS_BY_CR
from src.helpers import generate_list_of_dictionaries, get_average_dice

class CreatureMaker:
    """
    Handles creature design logic.
    """
    def __init__(self):
        self.cr_stats = generate_list_of_dictionaries(MONSTER_STATISTICS_BY_CR)

    def calculate_expected_cr(self, creature):
        """
        Tries to determine what CR given creature is.
        Returns (expected_cr, difference)
        """
        creature_stats = {
            "Hit Points": self.retrieve_stat_from_creature("Hit Points", creature),
            "Armor Class": self.retrieve_stat_from_creature("Armor Class", creature),
            "High Attack": self.retrieve_stat_from_creature("attack", creature),
            "Average Damage": self.retrieve_stat_from_creature("damage", creature),
        }
        expected_cr_stats = {}
        next_lowest_hp = 0
        next_highest_hp = 0
        next_lowest_ac = 0
        next_highest_ac = 0
        next_lowest_attack = 0
        next_highest_attack = 0
        next_lowest_damage_high = 0
        next_lowest_damage_low = 0
        next_highest_damage_high = 0
        next_highest_damage_low = 0

        monster_stats_by_cr = generate_list_of_dictionaries(MONSTER_STATISTICS_BY_CR)
        expected_cr_stats = {
            "Hit Points":0,
            "Armor Class":0,
            "High Attack":0,
            "Average Damage":0,
        }

        for entry in monster_stats_by_cr:
            # For every stat, if it is higher than the entry in monster statistics by cr:
            # Set the expected CR for that stat to that CR

            # Hit Points
            if int(creature_stats["Hit Points"]) >= int(entry["Hit Points"]):
                expected_cr_stats["Hit Points"] = entry["CR"]
                next_lowest_hp = int(entry["Hit Points"])
            else:
                next_highest_hp = int(entry["Hit Points"])

            # Armor Class
            if int(creature_stats["Armor Class"]) >= int(entry["Armor Class"]):
                expected_cr_stats["Armor Class"] = entry["CR"]
                next_lowest_ac = int(entry["Armor Class"])
            else:
                next_highest_ac = int(entry["Armor Class"])

            # ATTACK VALUES BASED OFF OF PHYSICAL COMBATANTS, MELEE OR RANGED
            # NOT CREATURES RELYING ON SPELLCASTING OR SPELL-LIKE ABILITIES TO DEAL DAMAGE
            # Attack Bonus
            if int(creature_stats["High Attack"]) >= int(entry["High Attack"]):
                expected_cr_stats["High Attack"] = entry["CR"]
                next_lowest_attack = int(entry["High Attack"])
            else:
                next_highest_attack = int(entry["High Attack"])

            # DAMAGE VALUES BASED OFF OF CREATURES THAT DEAL DAMAGE.
            # I AM NOT INTERESTED IN RP CREATURES THAT DON'T DEAL DAMAGE FOR CR CALCULATIONS.
            # Average Damage
            if int(creature_stats["Average Damage"]) >= int(entry["Average Damage High"] or int(entry["Average Damage Low"])):
                expected_cr_stats["Average Damage"] = entry["CR"]
                next_lowest_damage_high = int(entry["Average Damage High"])
                next_lowest_damage_low = int(entry["Average Damage Low"])
            else:
                next_highest_damage_high = int(entry["Average Damage Low"])
                next_highest_damage_low = int(entry["Average Damage Low"])

        return self.get_average_integer_from_dictionary(expected_cr_stats)

    def get_average_integer_from_dictionary(self, dictionary_with_int_values):
        """
        Returns average integer value rounded down
        from given dictionary that only contains integer values
        """
        cr_valued_stats = list(dictionary_with_int_values.values())
        expected_cr = 0
        for value in cr_valued_stats:
            expected_cr += int(value)
        expected_cr = int(expected_cr / len(cr_valued_stats))

        return expected_cr

    def retrieve_stat_from_creature(self, stat, creature):
        """
        Return the requested stat from creature
        """
        average_attack_bonus = 0
        for attack in creature.attacks:
            average_attack_bonus += sum(attack.attack_bonuses.values())
        # AVERAGE ATTACK BONUS ROUNDED DOWN
        average_attack_bonus = int((average_attack_bonus / len(creature.attacks)) // 1)
        ### DIVIDE BY ZERO IF 0 ATTACKS ON ABOVE LINE, NEEDS TO FIX??? 0 ATTACKS IMPOSSIBLE???

        stat_map = {
            "Hit Points": creature.secondary_attributes.get_hit_points(creature.hp_ability_score)[0],
            "Armor Class": creature.get_armor_class(),
            "attack": average_attack_bonus,
            "damage": creature.damage
        }
        return stat_map[stat]

    def find_highest_attack_bonus(self, creature):
        """
        finds the highest attack bonus for the creature
        """
        attack_bonus = creature.attack
        return attack_bonus

    def calculate_total_damage_for_attacks(self, creature):
        """
        returns the total damage for all attacks of creature
        """
        total_damage = creature.damage
        return total_damage

    def get_average_damage_from_all_attacks(self, creature):
        """
        returns the total average damage for all attacks of creature.
        """
        damage_total = 0
        ### NEED TO IMPLEMENT MULTIPLE ATTACKS FOR MANUFACTURED WEAPONS
        for attack in creature.attacks:
            damage_bonus_ability_score = creature.ability_scores.get_ability_modifier(attack.damage_ability_score)
            if damage_bonus_ability_score > 0:
                damage_bonus_ability_score = str(f'+{damage_bonus_ability_score}')
            elif damage_bonus_ability_score < 0:
                damage_bonus_ability_score = str(f'-{damage_bonus_ability_score}')
            else:
                damage_bonus_ability_score = ""
            damage_total += get_average_dice(attack.damage_dice)
