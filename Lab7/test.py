import unittest
from main import Config, success, another_try, back, momentary_insuccess, advance, expand, grammar


class TestParserFunctions(unittest.TestCase):
    def setUp(self):
        grammar.read_from_file("g1.txt")

    def test_expand(self):
        config = Config("normal state", 1, "", "S")
        config = expand(config)
        self.assertEqual(config.working_stack, "S1")
        self.assertEqual(config.input_stack, "aSbS")  # Assuming E is the nonterminal in the grammar

    def test_advance(self):
        config = Config("normal state", 1, "S1", "aSbS")
        config = advance(config)
        self.assertEqual(config.working_stack, "S1a")
        self.assertEqual(config.input_stack, "SbS")

    def test_momentary_insuccess(self):
        config = Config("normal state", 1, "", "S")
        config = momentary_insuccess(config)
        self.assertEqual(config.state, "back state")

    def test_back(self):
        config = Config("normal state", 1, "S1a", "SbS")
        config = back(config)
        self.assertEqual(config.length, 0)
        self.assertEqual(config.working_stack, "S1")
        self.assertEqual(config.input_stack, "aSbS")

    def test_another_try(self):
        config = Config("normal state", 2, "S1aS2", "aSbS")
        config = another_try(config)
        self.assertEqual(config.state, 'normal state')
        self.assertEqual(config.working_stack, 'S1aS3')
        self.assertEqual(config.input_stack, 'cbS')

    def test_success(self):
        config = Config("normal state", 1, "", "S")
        config = success(config)
        self.assertEqual(config.state, "final state")

if __name__ == '__main__':
    unittest.main()

