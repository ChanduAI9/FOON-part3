import random
from collections import deque
import math

class TreeNode:
    def __init__(self, state, parent=None, actions=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.success_count = 0
        self.actions = actions or []

    def add_child(self, child_state, child_actions):
        child = TreeNode(state=child_state, parent=self, actions=child_actions)
        self.children.append(child)
        return child

# Functions to parse
def load_foon_data(filename):
    foon_data = []
    with open(filename, 'r') as file:
        current_unit = {}
        for line in file:
            parts = line.strip().split()
            if not parts:
                continue
            if parts[0] == "O":
                current_unit['object'] = parts[1]
            elif parts[0] == "S":
                current_unit['state'] = parts[1:]
            elif parts[0] == "M":
                current_unit['action'] = parts[1]
            elif parts[0] == "//":
                foon_data.append(current_unit)
                current_unit = {}
    return foon_data

def load_kitchen_data(filename):
    with open(filename, 'r') as file:
        kitchen_items = [line.strip() for line in file.readlines()]
    return kitchen_items

def load_motion_success_rates(filename):
    success_rates = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                motion, rate = parts
                success_rates[motion] = float(rate)
    return success_rates

def simulate_task(task_tree, actions, success_rates, attempts):
    success_count = 0
    for _ in range(attempts):
        if execute_random(task_tree, actions, success_rates):
            success_count += 1
    return success_count / attempts

def execute_random(task_tree, actions, success_rates):
    for action in actions:
        if random.random() > success_rates.get(action, 0):
            return False
    return True

def run_mcts(root, success_rates, iterations=1000):
    for _ in range(iterations):
        node = select_best_node(root)
        expand_node(node)
        success = simulate_task(node.state, node.actions, success_rates, 1)
        propagate_results(node, success)

def select_best_node(node):
    while node.children:
        node = choose_best_child(node)
    return node

def choose_best_child(node, exploration_param=1.4):
    total_simulations = node.visits

    def compute_score(child):
        if child.visits == 0:
            return float('inf')
        average_success = child.success_count / child.visits
        exploration_term = exploration_param * (math.sqrt(math.log(total_simulations) / child.visits))
        return average_success + exploration_term

    return max(node.children, key=compute_score)

def expand_node(node):
    new_state, new_actions = create_new_state(node.state)
    node.add_child(new_state, new_actions)

def propagate_results(node, success):
    while node:
        node.visits += 1
        node.success_count += success
        node = node.parent

def create_new_state(current_state):
    if current_state == "raw egg":
        new_state = "whisked egg"
        new_actions = ["whisk"]
    elif current_state == "whisked egg":
        new_state = "cooking egg"
        new_actions = ["pour", "cook"]
    elif current_state == "cooking egg":
        new_state = "omelette"
        new_actions = ["serve"]
    else:
        new_state = "raw egg"
        new_actions = ["crack"]
    return new_state, new_actions

def display_tree(node):
    queue = deque([(node, 0)])
    while queue:
        current_node, level = queue.popleft()
        indent = "  " * level
        print(f"{indent}State: {current_node.state}, Visits: {current_node.visits}, Successes: {current_node.success_count}, Actions: {current_node.actions}")
        for child in current_node.children:
            queue.append((child, level + 1))

def save_tree_to_file(node, filename):
    with open(filename, "w") as f:
        queue = deque([(node, 0)])
        while queue:
            current_node, level = queue.popleft()
            if level > 0:
                f.write("//\n")
            f.write(f"O  {current_node.state}\n")
            f.write(f"S  {' '.join(current_node.actions)}\n")
            if current_node.actions:
                f.write(f"M  {', '.join(current_node.actions)}\n")
            for child in current_node.children:
                queue.append((child, level + 1))

if __name__ == "__main__":
    foon_data = load_foon_data("FOON.txt")
    kitchen_items = load_kitchen_data("kitchen.txt")
    motion_success_rates = load_motion_success_rates("motion.txt")

    goal_nodes = ["omelette", "pancake", "salad", "sandwich", "soup"]

    for goal in goal_nodes:
        root_node = TreeNode(state=goal, actions=["initial_action"])
        run_mcts(root_node, motion_success_rates, iterations=1000)
        output_filename = f"mcts_tree_{goal}.txt"
        save_tree_to_file(root_node, output_filename)
        print(f"\nMCTS Tree for {goal} saved to '{output_filename}'")
