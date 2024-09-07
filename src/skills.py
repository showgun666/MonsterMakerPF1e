#!/usr/bin/env python3
"""
Class for skills
"""
import src.helpers as helper_module
import src.exceptions as exceptions_module
from src.constants import SKILL_LIST

class Skills:
    "Skills class for creature"
    def __init__(self, class_skill_list):
        self.skills = helper_module.generate_list_of_dictionaries(SKILL_LIST)
        self.class_skills_list = class_skill_list

    """    def set_class_skills_list(self):
        "sets class skills according to type"
        type_class_skills = self.class_skills_list
        i = len(type_class_skills) - 1
        while i >= 0:
            if "Knowledge (pick one)" == type_class_skills[i]:
                # PICK A KNOWLEDGE THAT IS NOT A CLASS SKILL
                # FOR NOW WE JUST POP IT. IT IS BROKEN
                # FIX THIS LATER
                type_class_skills.pop(i)
                i -= 1
            elif "plus" in type_class_skills[i]:
                # FIX THIS ANOTHER TIME
                # ONE CASE IS FOR CLASS SKILLS COMBINED WITH CREATURE TYPE
                # ONE CASE IS FOR OUTSIDERS THAT HAVE +4
                type_class_skills.pop(i)
            elif "Knowledge (all)" in type_class_skills[i]:
                type_class_skills.pop(i)
                for skill in self.skills:
                    if "Knowledge" in skill["Skill"]:
                        type_class_skills.append(skill["Skill"])
        return type_class_skills"""

    def add_class_skills(self, given_class_skills_list):
        "Adds list of given class skills to the creature class skill list"
        # append class skills from type to self.class_skills_list
        for class_skill in given_class_skills_list:
            if class_skill not in self.class_skills_list:
                self.class_skills_list.append(class_skill)

    def set_class_skills(self, class_skills):
        "Sets class skills for creature."
        self.class_skills_list = class_skills

    def add_ranks_to_skill(self, skill, ranks=1):
        "adds ranks to skill"
        for entry in self.skills:
            if entry["Skill"] == skill:
                self.skills[skill] = str(int(entry[skill]) + ranks)
            else:
                raise exceptions_module.SearchMiss(f'Skill "{skill}" not found in skill list!')

    def get_skill(self, skill):
        "returns skill dictionary"
        return self.skills[skill]

    def add_new_skill(self, skill, untrained, armor_check_penalty, key_ability):
        "add a new skill to list"
        self.skills.append(
            {
                "Skill":skill,
                "Untrained":untrained,
                "Armor Check Penalty":armor_check_penalty,
                "Key Ability":key_ability,
            }
        )
