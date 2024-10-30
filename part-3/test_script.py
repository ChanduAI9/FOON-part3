import unittest
from mcts_algorithm import TreeNode, run_mcts, load_foon_data, load_kitchen_data, load_motion_success_rates, simulate_task, display_tree


class TestMCTSAlgorithm(unittest.TestCase):

    def setUp(self):
        self.foon_data = [
            {"object": "onion", "state": ["whole"], "motion": "chop"},
            {"object": "onion", "state": ["chopped"], "motion": "mix"},
        ]
        self.kitchen_items = ["onion", "knife", "bowl"]
        self.motion_success_rates = {
            "chop": 0.9,
            "mix": 0.8,
            "crack": 0.7,
            "beat": 0.6
        }
        self.root = TreeNode(state="omelette", actions=[
                             "crack", "beat", "pour"])

    def test_node_creation(self):
        """ Test if TreeNode creation works correctly """
        node = TreeNode(state="egg", actions=["crack"])
        self.assertEqual(node.state, "egg")
        self.assertEqual(node.actions, ["crack"])
        self.assertEqual(node.visits, 0)
        self.assertEqual(node.success_count, 0)
        self.assertEqual(len(node.children), 0)

    def test_simulation(self):
        """ Test simulate_task function """
        result = simulate_task(
            "omelette", ["crack", "beat"], self.motion_success_rates, 100)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_mcts_process(self):
        """ Test the run_mcts process runs without errors """
        run_mcts(self.root, self.motion_success_rates, iterations=100)
        self.assertGreater(self.root.visits, 0)
        self.assertGreaterEqual(self.root.success_count, 0)
        self.assertGreater(len(self.root.children), 0)

    def test_tree_structure(self):
        """ Test if the tree structure is correct after run_mcts """
        run_mcts(self.root, self.motion_success_rates, iterations=100)
        self.assertGreater(len(self.root.children), 0)
        for child in self.root.children:
            self.assertIsInstance(child.state, str)
            self.assertIsInstance(child.actions, list)
            self.assertGreaterEqual(child.visits, 0)
            self.assertGreaterEqual(child.success_count, 0)

    def test_tree_output(self):
        """ Test the display_tree function for output """
        run_mcts(self.root, self.motion_success_rates, iterations=50)
        print("\nTree structure after 50 iterations:")
        display_tree(self.root)

    def test_file_parsing(self):
        """ Test if files are parsed correctly """
        foon_data = load_foon_data("FOON.txt")
        kitchen_items = load_kitchen_data("kitchen.txt")
        motion_success_rates = load_motion_success_rates("motion.txt")
        self.assertIsInstance(foon_data, list)
        self.assertIsInstance(kitchen_items, list)
        self.assertIsInstance(motion_success_rates, dict)
        self.assertGreater(len(foon_data), 0)
        self.assertGreater(len(kitchen_items), 0)
        self.assertGreater(len(motion_success_rates), 0)


if __name__ == '__main__':
    unittest.main()
