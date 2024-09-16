#!/usr/bin/env python3
#pylint: disable=protected-access
"Test module for skills class"

import unittest
from src.skills import Skills
from src.exceptions import SearchMiss
from src.constants import CON, DEX

class TestSkills(unittest.TestCase):
    """class for testing the skills class, submodule for unittests. derives from unittest.TestCase"""
    def setUp(self):
        """ Create object for all tests """
        class_skills_list = [
            'Acrobatics',
            'Diplomacy',
            'Knowledge ("Nobility")',
            'Use Magic Device',
            ]
        self.skills = Skills(class_skills_list)

    def tearDown(self):
        """ Remove dependencies after test """
        self.skills = None

    def test_init(self):
        """init works as expected"""
        self.assertEqual(self.skills.class_skills_list[0], 'Acrobatics')
        self.assertTrue(isinstance(self.skills._skills, list))
        self.assertTrue(isinstance(self.skills._skills[0], dict))
        self.assertEqual("Acrobatics", self.skills._skills[0]["Skill"])
        self.assertEqual(self.skills._skills[0]["Skill Ranks"], 0)

        self.assertEqual(self.skills.find_skill("Acrobatics")["Skill"], "Acrobatics")
        self.assertEqual(self.skills.find_skill("Acrobatics")["Untrained"], True)
        self.assertEqual(self.skills.find_skill("Acrobatics")["Armor Check Penalty"], True)
        self.assertEqual(self.skills.find_skill("Acrobatics")["Key Ability"], DEX)


    def test_set_class_skills(self):
        """can set new class skill list"""
        new_class_skills = ["Climb", "Intimidate", "Ride"]
        self.skills.set_class_skills(new_class_skills)
        self.assertFalse("Acrobatics" in self.skills.class_skills_list)
        self.assertTrue("Climb" in self.skills.class_skills_list)

    def test_add_ranks_to_skill(self):
        """can add ranks to skills"""
        self.skills.add_skill_ranks("Acrobatics", 3)
        self.skills.add_skill_ranks("Acrobatics", 3)
        self.skills.add_skill_ranks("Diplomacy", 2)
        self.assertEqual(self.skills._skills[0]["Skill Ranks"], 6)
        self.assertEqual(self.skills._skills[5]["Skill Ranks"], 2)
        self.skills.add_skill_ranks("Acrobatics", -3)
        self.assertEqual(self.skills._skills[0]["Skill Ranks"], 3)

    def test_add_ranks_to_skill_miss_exception(self):
        """Trying to get a skill that doesn't exist raises SearchMiss"""
        with self.assertRaises(SearchMiss):
            self.skills.add_skill_ranks("Carousing", 1)

    def test_find_skill(self):
        """can get selected skill"""
        self.assertEqual(self.skills.find_skill("Acrobatics")["Skill"], "Acrobatics")

    def test_get_skill_search_miss_exception(self):
        """Trying to get a skill that doesn't exist raises SearchMiss"""
        with self.assertRaises(SearchMiss):
            self.skills.find_skill("Carousing")

    def test_add_new_skill(self):
        """can add new skill"""
        self.skills.add_new_skill("Carousing", True, False, CON)
        self.assertEqual(self.skills.find_skill("Carousing")["Skill"], "Carousing")
        self.assertEqual(self.skills.find_skill("Carousing")["Untrained"], True)
        self.assertEqual(self.skills.find_skill("Carousing")["Armor Check Penalty"], False)
        self.assertEqual(self.skills.find_skill("Carousing")["Key Ability"], CON)

    def test_remove_skill(self):
        """Can remove a skill"""
        self.skills.remove_skill("Acrobatics")
        with self.assertRaises(SearchMiss):
            self.skills.find_skill("Acrobatics")

    def test_remove_skill_search_miss_exception(self):
        """Trying to remove skill that doesn't exist raises searchmiss exception"""
        with self.assertRaises(SearchMiss):
            self.skills.remove_skill("Carousing")
