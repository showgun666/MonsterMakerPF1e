#!/usr/bin/env python3
"""
Class for skills
"""
import src.helpers as helper_module
from src.constants import * # Continuously check that this * import is not loading unneccessary stuff.

class Skills:
    "Skills class for creature"
    def __init__(self, class_skill_list):
        self.skills = helper_module.generate_list_of_dictionaries(SKILL_LIST)
        self.class_skills_list = class_skill_list

    def get_class_skills_by_type(self):
        "sets class skills according to type"
        if self.creature_type_statistics["Class Skills"] != "None":
            type_class_skills = self.creature_type_statistics["Class Skills"].split(", ")

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
        return type_class_skills

    def add_class_skills(self, given_class_skills_list):
        "Adds list of given class skills to the creature class skill list"
        # append class skills from type to self.class_skills_list
        for class_skill in given_class_skills_list:
            if class_skill not in self.class_skills_list:
                self.class_skills_list.append(class_skill)

    def set_class_skills(self, class_skills):
        "Sets class skills for creature."
        self.class_skills_list = class_skills

    def get_creature_type_dictionary(self, creature_type):
        "get the dictionary for a specific creature type"
        creature_by_type = helper_module.generate_list_of_dictionaries(CREATURE_STATISTICS_BY_TYPE)
        for creature_type_dictionary in creature_by_type:
            if creature_type_dictionary["Type"] == creature_type:
                return creature_type_dictionary
