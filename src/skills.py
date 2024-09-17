#!/usr/bin/env python3
"""
Class for skills
"""
import src.helpers as helper_module
import src.exceptions as exceptions_module
from src.constants import SKILL_LIST, STR, DEX, CON, INT, WIS, CHA

class Skills:
    "Skills class for creature"
    def __init__(self, class_skill_list):
        self._skills = helper_module.generate_list_of_dictionaries(SKILL_LIST)
        self.class_skills_list = class_skill_list

        for skill in self._skills:
            skill["Skill Ranks"] = int(skill["Skill Ranks"])
            if skill["Untrained"] == "Yes":
                skill["Untrained"] = True
            else:
                skill["Untrained"] = False

            if skill["Armor Check Penalty"] == "Yes":
                skill["Armor Check Penalty"] = True
            else:
                skill["Armor Check Penalty"] = False

            if skill["Key Ability"] == "Str":
                skill["Key Ability"] = STR
            elif skill["Key Ability"] == "Dex":
                skill["Key Ability"] = DEX
            elif skill["Key Ability"] == "Con":
                skill["Key Ability"] = CON
            elif skill["Key Ability"] == "Int":
                skill["Key Ability"] = INT
            elif skill["Key Ability"] == "Wis":
                skill["Key Ability"] = WIS
            elif skill["Key Ability"] == "Cha":
                skill["Key Ability"] = CHA
            else:
                raise exceptions_module.SearchMiss(f'''
{skill["Key Ability"]} not a legal key ability score.
                                                   ''')
            skill["Modifier"] = 0 ### <--- NEED TO WRITE TEST FOR THIS PART

    def add_class_skills(self, given_class_skills_list):
        "Adds list of given class skills to the creature class skill list"
        # append class skills from type to self.class_skills_list
        for class_skill in given_class_skills_list:
            if class_skill not in self.class_skills_list:
                self.class_skills_list.append(class_skill)

    def set_class_skills(self, class_skills):
        "Sets class skills for creature."
        self.class_skills_list = class_skills

    def find_skill(self, skill):
        """Finds given skill"""
        for entry in self._skills:
            if entry["Skill"] == skill:
                return entry
        raise exceptions_module.SearchMiss(f'Skill "{skill}" not found')

    def add_skill_ranks(self, skill, ranks=1):
        "adds ranks to skill, to subtract att negative number"
        found_skill = self.find_skill(skill)
        if skill == found_skill["Skill"]:
### SHOULD NOT BE ABLE TO ADD SKILL RANKS HIGHER THAN AMOUNT OF HD
            found_skill["Skill Ranks"] += ranks
            return
        raise exceptions_module.SearchMiss(f'Skill "{skill}" not found in skill list!')

    def add_new_skill(self, skill, untrained, armor_check_penalty, key_ability):
        "add a new skill to list"
        self._skills.append(
            {
                "Skill":skill,
                "Untrained":untrained,
                "Armor Check Penalty":armor_check_penalty,
                "Key Ability":key_ability,
            }
        )

    def remove_skill(self, skill):
        """Remove a skill. returns skill name popped"""
        for i, _ in enumerate(self._skills):
            if self._skills[i]["Skill"] == skill:
                return self._skills.pop(i)
        raise exceptions_module.SearchMiss(f'Skill "{skill}" not found in skill list!')
