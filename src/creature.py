#!/usr/bin/env python3
"""
Class for creature
"""
from typing import Optional
import src.ability_scores as ability_scores_class
import src.creature_type as creature_type_class
import src.skills as skills_class
import src.hit_dice as hit_dice_class
import src.secondary_attributes as secondary_attributes_class
import src.statSheet as stat_sheet_class
import src.helpers as helper_module
from src.exceptions import SearchMiss
from src.attack import Attack
from src.constants import CREATURE_SIZES, EXPERIENCE_POINT_AWARDS, CON, CHA, DEX

class Creature:
    "Class for creatures"
    def __init__(self, creature_type="Humanoid", cr="1", size="Medium"):
        creature_type = creature_type_class.CreatureType(creature_type)

        self.set_cr(cr)
        self.hit_dice = hit_dice_class.HitDice()
        self.ability_scores = ability_scores_class.AbilityScores()
        self.skills = skills_class.Skills(creature_type)
        self.melee_attacks = {}
        self.natural_attacks = {}
        self.ranged_attacks = {}
        self._size = size
        self.hp_ability_score = CON # Default Constitution
        self._damage = 0
        if creature_type == "Undead":
            self.hp_ability_score = CHA # Undead are Charisma

        #### CONSIDER CACHING SKILL MODIFIERS AND SKILLS EVERY TIME THEY CHANGE
        ####  IF THIS DATA WILL BE CHANGED OFTEN

        self.ac_bonuses = [
            int(self.size["Size Modifier"]), #Size bonus
                           ]
        #### PROBABLY NEED ATTACK GROUPS, LIKE NATURAL ATTACKS + MANUFACTURED ATTACKS AND MANUFACTURED/NATURAL ATTACKS?
        self.attacks = []
        i = int(creature_type.hit_dice_by_cr(self.get_cr()))
        while i > 0:
            self.hit_dice.add_hit_die(str(creature_type))

            i -= 1
        self.secondary_attributes = secondary_attributes_class.SecondaryAttributes(
            self.ability_scores, self.size["Creature Size"], self.hit_dice)
        #self._size = self.get_size_data()
        # Sizes fine, diminutive, tiny, small, medium, large, huge, gargantuan, colossal

        # self.update_statistics_by_hit_dice()

    @property
    def size(self):
        """
        Getter method for size dictionary of creature
        """
        return self._size

    @size.setter
    def size(self, given_size):
        """
        Setter method for size dictionary of creature
        """
        sizes = helper_module.generate_list_of_dictionaries(CREATURE_SIZES)
        for size in sizes:
            if size["Creature Size"] == given_size:
                self._size = size

    def set_cr(self, given_cr):
        "sets cr value"
        ### UPDATE HD?
        ### SET HD AGAIN?
        self._cr = given_cr

    def get_cr(self):
        "get cr value"
        return self._cr

    def get_skill_modifier(self, skill):
        """get modifier to d20 roll for select skill"""
        # ENCUMBERMENT?
        skillmod = 0
        skill = self.skills.find_skill(skill)

        skillmod += skill["Skill Ranks"]
        skillmod += self.ability_scores.get_ability_modifier(skill["Key Ability"])
        if skill in self.skills.class_skills_list:
            skillmod += 3
        if skill == "Stealth":
            skillmod += self.size["Size Modifier to Stealth"]
        #### FLY SKILL MANEUVERABILITY + SIZE

        return skillmod

    def get_d20pfsrd_stat_block(self):
        """create d20pfsrd format stat block as .txt file"""
        return stat_sheet_class.StatBlock(self).generate_stat_block_string_d20pfsrd()

    """    def update_statistics_by_hit_dice(self):
        "updates statistics based off of hd"
        # Feats by hd
        self._feats_from_hd = str((int(self.get_hd()) // 2) + 1)
        # Skill ranks
        self._skill_ranks_from_hd = int(self.creature_type_statistics["Skill Ranks"]) * int(self.get_hd())
        # saves
        # hp
        # bab
        self._bab = str(int(bool(self.creature_type_statistics["Base Attack Bonus (BAB)"]) * int(self.get_hd()) // 1))
        # bab updates cmb and cmd
        # DCs
        # Ability Scores for creatures with class levels
    """


    def get_xp_reward_by_cr(self, given_cr):
        """
        return:str  XP value for given_cr
        """
        xp_dictionary = helper_module.generate_list_of_dictionaries(EXPERIENCE_POINT_AWARDS)

        for index in xp_dictionary:
            if index["CR"] == str(given_cr):
                return index["Total XP"]

    def find_saves(self):
        """
        Retrieve saves
        """
        return self.hit_dice.saves_from_hit_dice()

    def add_natural_attack(self, attack, ability_attack, ability_damage):
        """
        Add a natural attack to self.natural_attacks
        """

    def add_attack(self,
            weapon:dict, base_attack_bonus:int, attack_mod:int,
            damage_mod:int, tags:list, size:str
            ) -> Attack:
        """
        Add an attack to creature
        """
        weapon_title = list(weapon.keys())[0]
        name = next(iter(weapon.values()))
        tags = []
        special = None
        if "Natural" in weapon_title:
            crit_range = [20]
            crit_multiplier = 2
            tags.append(weapon["Attack Type"])
        else:
            special = weapon["Special"].split(", ")
            if "20" not in weapon["Critical"]:
                crit_range = [20]
                crit_multiplier = int(weapon["Critical"].lstrip("x"))
            else:
                critlist = weapon["Critical"].split("x")
                crit_range = list(critlist[0])
                crit_multiplier = critlist[1]

        damage_types = weapon["Type"].split(" ")
        if "or" in damage_types:
            damage_types.remove("or")
        if "and" in damage_types:
            damage_types.remove("and")
        if "Light" in weapon_title:
            tags.append("finesse")
            tags.append("manufactured")
        if "Two-Handed" in weapon_title:
            tags.append("two_handed")
            tags.append("manufactured")
        if "Melee" in weapon_title:
            tags.append("melee")
        if "Unarmed" in weapon_title:
            tags.append("unarmed")
        if "Simple" in weapon_title:
            tags.append("simple")
            tags.append("manufactured")
        if "Martial" in weapon_title:
            tags.append("martial")
            tags.append("manufactured")
        if "Exotic" in weapon_title:
            tags.append("exotic")
            tags.append("manufactured")
        if "Crossbow" in weapon_title:
            tags.append("crossbow")
            tags.append("manufactured")
        elif "bow" in weapon_title:
            tags.append("bow")
            tags.append("manufactured")
        if "Natural" in weapon_title:
            tags.append("natural")
        ### FIGHTER WEAPON GROUPS

        ### PENALTIES & BONUSES TO ATTACK BONUS
        attack_modifiers = {}
        ### SIZE BONUS/PENALTY
        size_dictionary = helper_module.generate_list_of_dictionaries(CREATURE_SIZES)
        for size_cat in size_dictionary:
            if size_cat == self.size:
                attack_modifiers["Size Modifier"] = int(size_cat["Size Modifier"])

        ### ABILITY SCORE MODIFIER TO ATTACK
        attack_modifiers["Ability Modifier"] = self.ability_scores.get_ability_modifier(attack_mod)

        ### TAG PENALTIES
        ### NEED A TAG HANDLING METHOD THAT HANDLES ALL TAG THINGS WHEN CALCULATING THINGS
        if "Secondary" in tags:
            attack_modifiers["Secondary"] = -5

        ### ADD BAB
        attack_modifiers["BAB"] = base_attack_bonus

        attack = Attack(
            name=name,
            attack_bonuses=attack_modifiers,
            attack_ability_score=attack_mod,
            damage_dice=weapon["Dmg (M)"],
            damage_ability_score=damage_mod,
            critical_range=crit_range,
            critical_multiplier=crit_multiplier,
            damage_types=damage_types,
            special_abilities=special,
            tags=tags,
        )
        self.attacks.append(attack)
        ### Also add iterative attacks
        if "manufactured" in tags and base_attack_bonus >= 6:
            self.add_iterative_attacks(
                name,
                attack_modifiers,
                attack_mod,
                weapon["Dmg (M)"],
                damage_mod,
                crit_range,
                crit_multiplier,
                damage_types,
                special,
                tags,
                )

    def add_iterative_attacks(
            self,
            name,
            attack_modifiers,
            attack_mod,
            weapon_damage_dice,
            damage_mod,
            crit_range,
            crit_multiplier,
            damage_types,
            special,
            tags,
            ):
        """
        Adds iterative attacks based on first attack.
        """
        full_bab = attack_modifiers["BAB"]
        bab_bonus = full_bab
        while bab_bonus >= 1 and bab_bonus >= full_bab - 10:
            bab_bonus -= 5
            iterated_attack_modifiers_list = []
            iterated_attack_modifiers_list.append(attack_modifiers.copy())
            iterated_attack_modifiers_list[-1]["BAB"] = bab_bonus

            attack = Attack(
            name,
            iterated_attack_modifiers_list[-1],
            attack_mod,
            weapon_damage_dice,
            damage_mod,
            crit_range,
            crit_multiplier,
            damage_types,
            special,
            tags,
            )
            self.attacks.append(attack)

    def get_attack_by_name(self, name: str) -> Optional[Attack]:
        """Retrieve an attack by its name."""
        for attack in self.attacks:
            if attack.name == name:
                return attack
        return None

    def get_armor_class(self):
        """ Get AC of creature """
        return self.secondary_attributes.calculate_difficulty_class(ability_mod=DEX, bonuses=sum(self.ac_bonuses))

    def attack_string_representation(self, attack):
        """
        get string representation of attack
        e.g. Shortsword +3 1d6+3
        """
        posnegattack = "+"
        if attack.attack_bonus < 0:
            posnegattack = "-"
        posnegdmg = "+"
        if self.ability_scores.get_ability_modifier(attack.damage_ability_score) < 0:
            posnegdmg = "-"
        elif self.ability_scores.get_ability_modifier(attack.damage_ability_score) == 0:
            posnegdmg = "" # If no damage bonus modifier. Doesn't account for minor bonuses.

        return f'{attack.name} {posnegattack}{attack.attack_bonus} {posnegdmg}{attack.damage_dice}'

    @property
    def damage(self):
        """
        getter for damage
        """
        total_damage = 0
        for attack in self.attacks:
            total_damage += attack.calculate_weapon_damage(self.ability_scores)
        return total_damage

    @damage.setter
    def damage(self):
        """
        setter for damage
        """
        total_damage = 0
        for attack in self.attacks:
            total_damage += attack.calculate_weapon_damage(self.ability_scores)
        self._damage = total_damage

    def get_attack_bonus_average(self) -> float:
        """
        returns average attack bonus
        """
        attack_bonuses = []
        for attack in self.attacks:
            attack_bonuses.append(attack.calculate_attack_bonus(self))
        return sum(attack_bonuses) / len(attack_bonuses)
