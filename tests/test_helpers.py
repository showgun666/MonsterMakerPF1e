#!/usr/bin/env python3
#pylint: disable=protected-access
"Test module for Trie class"

import unittest
import src.helpers as helpers

TEXT_FILE = "src/tables/skillSummary.txt"

class TestHelpers(unittest.TestCase):
    "Class for testing helpers"

    def test_generate_skills_generates_correctly(self):
        "test that the function can generate skill list"

        skills = helpers.generate_list_of_dictionaries(TEXT_FILE)

        print(skills)
